package us.yuxin.examples.ingest;

import org.apache.hadoop.hbase.util.Bytes;

/**
 * Created with IntelliJ IDEA.
 * User: is
 * Date: 10/22/12
 * Time: 10:01 PM
 * To change this template use File | Settings | File Templates.
 */
public class Test {
  public static void main(String[] args) {
    System.out.println("String".getBytes().length);
    System.out.println(Bytes.toBytes("String").length);
  }
}
