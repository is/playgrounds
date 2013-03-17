package us.yuxin.chdbits

import java.net.URLEncoder

import dispatch.{:/, Http}
import com.typesafe.config.Config
import util.matching.Regex
import collection.mutable.ListBuffer
import java.io.FileOutputStream

class Feeder(username: String, password: String, depth: Int) {
  def this(username: String, password: String) = this(username, password, 5)

  def this(config: Config) = this(
    config.getString("username"),
    config.getString("password"),
    config.getInt("depth"))

  private val formType = "application/x-www-form-urlencoded"
  private val loginForm = "username=" + urlEncode(username) + "&password=" + urlEncode(password)
  val http = new Http

  private val baseUrl = :/ ("chdbits.org")
  // private val baseUrl = :/("chdbits.org").secure
  private val loginUrl = baseUrl / "takelogin.php"
  private val torrentsUrl = baseUrl / "torrents.php"
  private val downloadUrl = baseUrl / "download.php"


  private val rBig = """(?s)<tr>.{1,6}<td class="rowfollow nowrap" valign="middle" style='padding: 0px'>.+?</table>.+?</tr>""".r
  private val rDetail = new Regex(
    """(?m)(?s)img class="c_(.+?)" src=.+?addsprites.gif\);" alt="(.+?)".+? href="details.php\?id=(\d+)&amp;hit=1" ><b>""" +
      """(.+?)</b></a><br />(.+?)</td>.+?</span></td><td class="rowfollow">(.+?)<br />(.+?)</td>""" +
      """<td class="rowfollow" align="center">(.+?)</td>.+?<td class="rowfollow">(.+?)</td>.+?<td class="rowfollow">(.+?)</td>""" +
      """.+?<td class="rowfollow">(.+?)</td>""",
    "category", "encode", "id", "name", "desc", "size", "unit", "seeds", "leechs", "downloads", "publisher")
  private val rNumber = """>(\d+)<""".r
  private val rDesc = """(.+?) <img class="pro_(.+?)"""".r

  def urlEncode(s: String) = URLEncoder.encode(s, "utf8")


  def gbSize(size: String, unit: String): Float = {
    size.toFloat * (unit match {
      case "GB" => 1f
      case "MB" => 0.00097656f
    })
  }


  def toNumber(in: String): Int = {
    if (in == "0")
      0
    else {
      val m = rNumber.findFirstMatchIn(in)

      if (m.isEmpty)
        -1
      else
        m.get.group(1).toInt

    }
  }


  def login() = http(loginUrl <<(loginForm, formType) as_str)


  def torrents(id: Int) = http(torrentsUrl <<? Map("page" -> id.toString) as_str)


  def parseTorrentInfo(in: String): Option[ItemInfo] = rDetail.findFirstMatchIn(in) match {
    case None => None
    case Some(m) => {
      val (desc, rate) = {
        val d = m.group("desc")

        if (d.indexOf("<img") == -1)
          (d, "100")
        else {
          val dm = rDesc.findFirstMatchIn(d).get
          val rMap = Map("50pctdown" -> "50", "free" -> "free")
          (dm.group(1), rMap.getOrElse(dm.group(2), dm.group(2)))
        }
      }

      Some(new ItemInfo(
        m.group("id"), m.group("name"),
        m.group("category"),
        m.group("encode"), desc,
        rate, gbSize(m.group("size"), m.group("unit")),
        toNumber(m.group("seeds")),
        toNumber(m.group("leechs")),
        toNumber(m.group("downloads")),
        "anonymous"))
    }
  }

  def torrentInfos(): List[ItemInfo] = {
    val res = new ListBuffer[ItemInfo]
    for (i <- List.range(0, depth)) {
      rBig.findAllIn(torrents(i)).foreach {
        block =>
          val item = parseTorrentInfo(block)
          if (item.isDefined) {
            res += item.get
          }
      }
    }
    res.toList
  }

  def downloadTorrent(id:String, fn:String) = {
    val fos = new FileOutputStream(fn)
    http(downloadUrl <<? Map("id"->id) >>> fos)
    fos.close()
  }
}


