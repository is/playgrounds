package us.yuxin.chdbits


case class ItemInfo(id: String,
                    name: String, category: String, encode: String, desc: String,
                    rate: String, size: Float, seed: Int, leech: Int, download: Int, publisher: String) {

  lazy val torrentFilename = "%s__%s.torrent".format(id, name.replace(" ", "_"))
}