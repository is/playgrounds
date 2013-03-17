package us.yuxin.chdbits

import dispatch.{:/, Http, url}
import org.apache.http.impl.client.DefaultHttpClient
import com.typesafe.config.Config
import java.net.URLEncoder

class Feeder (username:String, password:String, depth:Int) {
  def this(username:String, password:String) = this(username, password, 5)

  def this(config:Config) = this(
    config.getString("username"),
    config.getString("password"),
    config.getInt("depth"))

  val http = new Http
  val contentType = "application/x-www-form-urlencoded"
  def urlEncode(s:String) = URLEncoder.encode(s, "utf8")

  def try0() = {
    val req = url("http://www.scala-lang.org")

    val h = new Http
    val handler = req >>> System.out
    h(handler )
  }

  def try1() = {
    val req = url("http://www.scala-lang.org")
    val handler = req >:> { _.foreach(println)}
    val h = new Http
    h(handler)
  }

  def try2() = {
    val h = new Http
    val s:String = h(url("http://www.scala-lang.org/") as_str)

    var hc:DefaultHttpClient = h.client.asInstanceOf[DefaultHttpClient]
    println(hc.getCookieStore)
  }

  def try3() = {
    val b = :/ ("www.scala-lang.org")
    val learnScala = b / "node" / "1305"

    val h = new Http

    val s = h(learnScala >:> {_.foreach(println)})
  }



  def try5() = {
    val req = url("https://www.chdbits.org/")
    val formStr = "username=" + urlEncode(username) + "&password=" + urlEncode(password)
    val s = http(req << (formStr, contentType) as_str)
    println(s)
  }
}
