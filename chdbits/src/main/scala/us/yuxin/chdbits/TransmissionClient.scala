package us.yuxin.chdbits

import net.liftweb.json._
import net.liftweb.json.JsonDSL._
import com.typesafe.config.Config
import dispatch.classic.{url, Http}

class TransmissionClient (cf:Config) {
  val http = Http
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

  def addTorrent(i:ItemInfo, torrent:Array[Byte]) = {
    val json =
      ("method" -> "torrent-add") ~
      ("arguments" ->
        ("paused" -> true) ~
        ("metainfo" -> new sun.misc.BASE64Encoder().encode(torrent).replace("\r", "").replace("\n", "")))

    val reqJson = compact(render(json))

    // println("send:" + reqJson)

    val res = http (req
        <:< Map("X-Transmission-Session-Id" -> sessionId)
        << (reqJson, "application/json") as_str)
    println(res)
  }
}
