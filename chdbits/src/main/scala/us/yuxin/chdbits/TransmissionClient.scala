package us.yuxin.chdbits

import net.liftweb.json._
import net.liftweb.json.JsonDSL._
import com.typesafe.config.Config
import dispatch.classic.{url, Http, Handler}

class TransmissionClient(cf: Config) {
  type HttpPackage[T] = T
  val http = Http
  var sessId: String = "unset"

  lazy val req = {
    val req = url(cf.getString("url"))
    if (cf.hasPath("username"))
      req.as(cf.getString("username"), cf.getString("password"))
    else
      req
  }

  def sessionId = {
    val s = http.x(req >:> identity)
    s.get("X-Transmission-Session-Id").get.head
  }

  // If Code == 409, Set X-Transmission-Session-Id and retry.
  def httpx[T](x: Handler[T]): HttpPackage[T] = {
    val hand = x.copy(request = x.request <:< Map("X-Transmission-Session-Id" -> sessId))

    var is409: Boolean = false
    val r = http.x(hand.copy(
      block = { (code, res, ent) =>
      if (code != 409)
        hand.block(code, res, ent)
      else {
        val st = Map.empty[String, Set[String]].withDefaultValue(Set.empty)
        sessId = ((st /: res.getAllHeaders()) { (m, h) =>
          m + (h.getName -> (m(h.getName) + h.getValue))
        }).get("X-Transmission-Session-Id").get.head
        is409 = true
        hand.block(code, res, ent)
      }
    }))

    if (!is409)
      r
    else
      httpx(x)
  }


  def addTorrent(i: ItemInfo, torrent: Array[Byte]) = {
    val json =
      ( "method" -> "torrent-add" ) ~
        ( "arguments" ->
          ( "paused" -> true ) ~
            ( "metainfo" -> new sun.misc.BASE64Encoder().encode(torrent).replace("\r", "").replace("\n", "") ) )

    val reqJson = compact(render(json))
    httpx(req <<(reqJson, "application/json") as_str)
  }

  def startTorrent(id:Int) = {
    val json =
      ("method" -> "torrent-start") ~
      ("arguments" ->
        ("ids" -> id))
    val reqJson = compact(render(json))
    httpx(req << (reqJson, "application/json") as_str)
  }
}
