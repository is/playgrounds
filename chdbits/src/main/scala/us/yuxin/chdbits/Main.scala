package us.yuxin.chdbits

import com.typesafe.config.ConfigFactory
import java.io.File

/**
 * @author ${user.name}
 */
object Main {
  
  def foo(x : Array[String]) = x.foldLeft("")((a,b) => a + b)
  
  def main(args : Array[String]) {
    val config = ConfigFactory.parseFile(new File("application.conf"))

    val feed = new Feeder(config)
    feed try5()
  }
}
