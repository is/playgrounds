package us.yuxin.chdbits

import java.net.URLEncoder

import dispatch.classic.{Handler, Http, :/}
import com.typesafe.config.Config
import util.matching.Regex
import collection.mutable.ListBuffer
import java.io.{ByteArrayOutputStream, FileOutputStream}

class Feeder(username: String, password: String, depth: Int) {
  def this(username: String, password: String) = this(username, password, 5)

  def this(config: Config) = this(
    config.getString("username"),
    config.getString("password"),
    config.getInt("depth"))

  private val httpRetry = 15

  private val formType = "application/x-www-form-urlencoded"
  private val loginForm = "username=" + urlEncode(username) + "&password=" + urlEncode(password)
  val http = new Http

  private val baseUrl = :/ ("chdbits.org")
  // private val baseUrl = url("chdbits.org").secure
  private val loginUrl = baseUrl / "takelogin.php"
  private val torrentsUrl = baseUrl / "torrents.php"
  private val downloadUrl = baseUrl / "download.php"


  private val rBig = """(?s)<tr.{1,26}<td class="rowfollow nowrap" valign="middle" style='padding: 0px'>.+?</table>.+?</tr>""".r
  private val rDetail = new Regex(
    """(?m)(?s)img class="c_(.+?)"""" + //category
    """ src=.+?addsprites.gif\);" alt="(.+?)"""" + //encode
    """.+? href="details.php\?id=(\d+)&amp;hit=1" ><b>""" + // id
    """(.+?)</b></a><br />(.+?)</td>""" + //name & desc
    """.+?alt="(Unbookmarked|Bookmarked)"""" + // bookmarked
    """.+?</span></td><td class="rowfollow">(.+?)<br />(.+?)</td>""" + // size & unit
    """<td class="rowfollow" align="center">(.+?)</td>""" +
    """.+?<td class="rowfollow">(.+?)</td>""" +
    """.+?<td class="rowfollow">(.+?)</td>""" +
    """.+?<td class="rowfollow">(.+?)</td>""",
    "category", "encode", "id", "name", "desc", "bookmarked", "size", "unit", "seeds", "leechs", "downloads", "publisher")
  private val rNumber = """>(\d+)<""".r
  private val rDesc = """(.*?) <img class="pro_(.+?)"""".r

  private def urlEncode(s: String) = URLEncoder.encode(s, "utf8")

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

  def httpx[T](handler:Handler[T]):T = httpx(handler, httpRetry)
  def httpx[T](handler:Handler[T], retry:Int):T = {
    http.x(handler.copy(
    block = {(code, res, ent) =>
      // println("code=" + code)
      if (code >= 500)
        httpx(handler, retry - 1)
      else
        handler.block(code, res, ent)
    }))
  }

  def login() = httpx(loginUrl <<(loginForm, formType) as_str)

  def torrents(id: Int) = httpx(torrentsUrl <<? Map("page" -> id.toString) as_str)


  def parseTorrentInfo(in: String): Option[ItemInfo] = rDetail.findFirstMatchIn(in) match {
    case None => None
    case Some(m) => {
      val (desc, rate) = {
        val d = m.group("desc")

        if (d.indexOf("<img") == -1)
          (d, "100")
        else {
          val cdm = rDesc.findFirstMatchIn(d)
          if (cdm == None) {
            println(d)
          }
          val dm = cdm.get
          val rMap = Map("50pctdown" -> "50", "free" -> "free")
          (dm.group(1), rMap.getOrElse(dm.group(2), dm.group(2)))
        }
      }

      Some(new ItemInfo(
        id = m.group("id"),
        name = m.group("name"),
        category = m.group("category"),
        encode = m.group("encode"),
        desc = desc,
        bookmarked = m.group("bookmarked") == "Bookmarked",
        rate = rate,
        size = gbSize(m.group("size"), m.group("unit")),
        seed = toNumber(m.group("seeds")),
        leech = toNumber(m.group("leechs")),
        download = toNumber(m.group("downloads")),
        publisher = "anonymous"))
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

//  def downloadTorrent(id:String, fn:String) = {
//    val fos = new FileOutputStream(fn)
//    httpx(downloadUrl <<? Map("id"->id) >>> fos)
//    fos.close()
//  }

  def downloadTorrent(id:String):Array[Byte] = {
    val bs = new ByteArrayOutputStream()
    httpx(downloadUrl <<? Map("id"->id) >>> bs)
    bs.close()
    bs.toByteArray()
  }
}
