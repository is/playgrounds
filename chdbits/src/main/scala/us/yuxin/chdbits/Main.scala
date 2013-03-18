package us.yuxin.chdbits

import com.typesafe.config.ConfigFactory
import java.io.{FileOutputStream, File}

/**
 * @author ${user.name}
 */
object Main {

  def foo(x: Array[String]) = x.foldLeft("")((a, b) => a + b)

  def main(args: Array[String]) {
    val config = ConfigFactory.parseFile(new File("application.json"))

    val feed = new Feeder(config.getConfig("chdbits"))

    val tc = new TransmissionClient(config.getConfig("transmission.ovh"))
    feed.login()
    feed.torrentInfos().filter({
      _.rate eq "free"
    }).foreach {
      i =>
        println("%s: [%s] %s - %.3f -- %s %d/%d/%d - %s".format(
          i.id, i.category, i.name, i.size, i.rate,
          i.seed, i.leech, i.download, i.bookmarked))
        val path = config.getString("download.path") + "/" + i.torrentFilename;
        if (!new File(path).exists()) {
          val torrent = feed.downloadTorrent(i.id)
          println("save to: " + i.torrentFilename)
          val fos = new FileOutputStream(path)
          fos.write(torrent)
          fos.close
          tc.addTorrent(i, torrent)
        } else {
          println("skipped")
        }
    }
  }
}
