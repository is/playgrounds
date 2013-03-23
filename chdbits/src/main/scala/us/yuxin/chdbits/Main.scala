package us.yuxin.chdbits

import com.typesafe.config.ConfigFactory
import java.io.{FileOutputStream, File}
import net.liftweb.json._

/**
 * @author ${user.name}
 */
object Main {
  def main(args: Array[String]) {
    val config = ConfigFactory.parseFile(new File("application.json"))

    val feed = new Feeder(config.getConfig("chdbits"))

    val tc = new TransmissionClient(
      config.getConfig("transmission").getConfig(
        config.getString("transmission.default")))
    
    feed.login()
    feed.torrentInfos().filter({ i=>
      (i.rate eq "free") && (!i.bookmarked)
    }).foreach {
      i =>
        println("%s: [%s] %s - %.3f -- %s %d/%d/%d".format(
          i.id, i.category, i.name, i.size, i.rate,
          i.seed, i.leech, i.download))
        val path = config.getString("download.path") + "/" + i.torrentFilename;
        if (!new File(path).exists()) {
          val torrent = feed.downloadTorrent(i.id)

          if (i.seed < 5 && i.seed >= 0) {
            val r = tc.addTorrent(i, torrent)
            print(r)
            val res = parse(r)

            if ((res \\ "result").values.toString() == "success" && i.size < config.getDouble("autostart")) {
              val id:Int =
                (res \\ "arguments" \\ "torrent-added" \\ "id").asInstanceOf[JInt].values.toInt
              print("-- torrent-started:" + tc.startTorrent(id))
            }
          }

          println("-- save-to: " + i.torrentFilename)
          val fos = new FileOutputStream(path)
          fos.write(torrent)
          fos.close()
        } else {
          // println("skipped")
        }
    }
  }
}
