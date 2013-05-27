package us.yuxin.chdbits

import com.typesafe.config.ConfigFactory
import java.io.{PrintWriter, FileOutputStream, File}
import net.liftweb.json._

/**
 * @author ${user.name}
 */
object MainT0 {
  def main(args: Array[String]) {
    val config = ConfigFactory.parseFile(new File("application.json"))

    val feed = new Feeder(config.getConfig("chdbits"))

    val tc = new TransmissionClient(
      config.getConfig("transmission").getConfig(
        config.getString("transmission.default")))
    
    feed.login()

    val page = feed.torrents(1)
    println(page)


    Some(new PrintWriter("page.html")).foreach{p => p.write(page); p.close}

  }
}
