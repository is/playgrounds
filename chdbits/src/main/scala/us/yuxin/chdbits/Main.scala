package us.yuxin.chdbits

import com.typesafe.config.ConfigFactory
import java.io.{FileOutputStream, File}

/**
 * @author ${user.name}
 */
object Main {
  def main(args: Array[String]) {
    val config = ConfigFactory.parseFile(new File("application.json"))

    val feed = new Feeder(config.getConfig("chdbits"))

    val tc = new TransmissionClient(config.getConfig("transmission.ovh"))
    feed.login()
    feed.torrentInfos().filter({ i=>
      (i.rate eq "free") && (!i.bookmarked)
    }).foreach {
      i =>
        println("%s: [%s] %s - %.3f -- %s %d/%d/%d - %s".format(
          i.id, i.category, i.name, i.size, i.rate,
          i.seed, i.leech, i.download, i.bookmarked))
        val path = config.getString("download.path") + "/" + i.torrentFilename;
        if (!new File(path).exists()) {
          val torrent = feed.downloadTorrent(i.id)

          if (i.seed < 5)
            tc.addTorrent(i, torrent)

          println("save to: " + i.torrentFilename)
          val fos = new FileOutputStream(path)
          fos.write(torrent)
          fos.close()
        } else {
          println("skipped")
        }
    }
  }
}
