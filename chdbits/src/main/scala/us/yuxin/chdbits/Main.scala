package us.yuxin.chdbits

import com.typesafe.config.ConfigFactory
import java.io.{FileOutputStream, File}

/**
 * @author ${user.name}
 */
object Main {

  def foo(x: Array[String]) = x.foldLeft("")((a, b) => a + b)

  def main(args: Array[String]) {
    val config = ConfigFactory.parseFile(new File("application.conf"))

    val feed = new Feeder(config)
    //    feed.login
    //
    //    println ("--0--")
    //    println (feed.torrents(0))
    //
    //    println ("--1--")
    //    println (feed.torrents(1))
    //    println (feed.http)

    //    val lines = scala.io.Source.fromFile("page0.html").mkString
    //    feed.rBig.findAllIn(lines).foreach { block =>
    //      var i = feed.parseTorrentInfo(block).get
    //
    //      println("%s: [%s] %s - %.3f".format(i.id, i.category, i.name,  i.size))
    //    }

    val tc = new TransmissionClient(config, "h6s")

    feed.login()


    feed.torrentInfos.filter({
      _.rate eq "free"
    }).foreach {
      i =>
        println("%s: [%s] %s - %.3f -- %s".format(i.id, i.category, i.name, i.size, i.rate))
        val path = config.getString("download.path") + "/" + i.torrentFilename;
        if (!new File(path).exists()) {
          feed.downloadTorrent(i.id, path)
          println("save to" + i.torrentFilename)
          val source = scala.io.Source.fromFile(path, "ISO-8859-1")
          val torrent = source.map(_.toByte).toArray
          source.close
          tc.addTorrent(i, torrent)
        } else {
          println("skipped")
        }
    }
  }
}
