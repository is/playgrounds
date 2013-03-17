package us.yuxin.chdbits

import net.liftweb.json._
import net.liftweb.json.JsonDSL._
import com.typesafe.config.Config
import dispatch.{url, Http}

class TransmissionClient (cf:Config, clientName:String) {
  val http = Http
  lazy val sessionId = {
    val s = http.x((url("http://ovh:9091/transmission/rpc") as("xx", "xxxxxxx")) >:> identity)
    s.get("X-Transmission-Session-Id").get.head
  }

  def addTorrent(i:ItemInfo, torrent:Array[Byte]) = {
    val json =
      ("method" -> "torrent-add") ~
      ("arguments" ->
        ("paused" -> true) ~
        ("metainfo" -> new sun.misc.BASE64Encoder().encode(torrent).replace("\n", "")))

    val reqJson = compact(render(json))

    println("send:" + reqJson)

    val res = http (
      (url("http://ovh:9091/transmission/rpc") as("xx", "xxxxxxx"))
        <:< Map("X-Transmission-Session-Id" -> sessionId)
        << (reqJson, "application/json") as_str)
    println(res)
  }
}
