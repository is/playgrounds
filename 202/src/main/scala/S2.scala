
object S2{
  def main(args: Array[String]) {
    var m:MersenneTwisterFast = new MersenneTwisterFast()
    m.setSeed(33333)

    m.nextDouble()
    for (a <- 1 to 100) {
      println(m.nextDouble())
    }

    var s:Double = 0
    var c:Int = 0
    val b0:Long = System.currentTimeMillis();
    for (a <- 1 to 10000000) {
      s = s + m.nextDouble()
      c = c + 1
      if (c % 10000 == 0) {
        println(c +  ":" + (s/c))
      }
    }
    val e0:Long = System.currentTimeMillis()
    println ((e0 - b0) + " ms")
  }
}
