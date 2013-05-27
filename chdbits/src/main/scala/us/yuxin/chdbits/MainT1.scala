package us.yuxin.chdbits

import scala.util.matching.Regex

/**
 * @author ${user.name}
 */
object MainT1 {
  def main(args: Array[String]) {
    val source = scala.io.Source.fromFile("page.html")
    val page = source.mkString
    source.close()

    val rBig = """(?s)<tr.{1,26}<td class="rowfollow nowrap" valign="middle" style='padding: 0px'>.+?</table>.+?</tr>""".r
    println (rBig.findFirstIn(page));

    println("--")
    rBig.findAllIn(page).foreach {block=>
      println(block)
      println(">>>>")
    }

    val S = rBig.findFirstIn(page).get


    println("------")
    println(S)
    println("------")

    val rDetail = new Regex(
      """(?m)(?s)img class="c_(.+?)"""" + //category
        """ src=.+?addsprites.gif\);" alt="(.+?)"""" + //encode
        """.+? href="details.php\?id=(\d+)&amp;hit=1" ><b>""" + // id
        """(.+?)</b></a>(.*?)<br />(.+?)</td>""" + //name & free & desc
        """.+?alt="(Unbookmarked|Bookmarked)"""" + // bookmarked
        """.+?</span></td><td class="rowfollow">(.+?)<br />(.+?)</td>""" + // size & unit
        """<td class="rowfollow" align="center">(.+?)</td>""" +
        """.+?<td class="rowfollow">(.+?)</td>""" +
        """.+?<td class="rowfollow">(.+?)</td>""" +
        """.+?<td class="rowfollow">(.+?)</td>""",
      "category", "encode", "id", "name", "free", "desc", "bookmarked", "size", "unit", "seeds", "leechs", "downloads", "publisher")

    val rDetail2 = new Regex(
      """(?m)(?s)img class="c_(.+?)"""" +
        """ src=.+?addsprites.gif\);" alt="(.+?)"""" +
        """.+? href="details.php\?id=(\d+)&amp;hit=1" ><b>""" +
        """(.+?)</b></a>(.*?)<br />(.+?)</td>""")

    println(rDetail2.findFirstIn(S))

    val rDetail3 = new Regex(
      """(?m)(?s)img class="c_(.+?)"""" + //category
        """ src=.+?addsprites.gif\);" alt="(.+?)"""")
    println(rDetail3.findFirstIn(S))


    println(rDetail.findFirstIn(S))
  }
}
