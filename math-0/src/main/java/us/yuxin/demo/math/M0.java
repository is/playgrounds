package us.yuxin.demo.math;

import java.util.Random;

public class M0 {
  public static void main(String argv[]) {
    MersenneTwisterFast r = new MersenneTwisterFast();


    int c30 = 0;
    int c300 = 0;
    int c600 = 0;
    int c3600 = 0;
    int c24 = 0;
    int c72 = 0;
    int cbig = 0;
    int max = 0;

    for (int i = 0; i < 100000; i++) {
      int m = second(r, 3600 * 144);

      if (m < 30)
        ++c30;
      else if (m < 300)
        ++c300;
      else if (m < 600)
        ++c600;
      else if (m < 3600)
        ++c3600;
      else if (m < 3600 * 24)
        ++c24;
      else if (m < 3600 * 72)
        ++c72;
      else
        ++cbig;

      if (m > max)
        max = m;
    }

    System.out.println(c30);
    System.out.println(c300);
    System.out.println(c600);
    System.out.println(c3600);
    System.out.println(c24);
    System.out.println(c72);
    System.out.println(cbig);

    System.out.println("--");
    System.out.println(max / 3600);
  }

  public static int second(MersenneTwisterFast r, int limit) {
    int ret = 0;
    do {
      float m0 = r.nextFloat();
      if (m0 < 0.4)
        ret = (int)Math.abs(r.nextGaussian() * 30 + 30);
      else if (m0 < 0.75)
        ret =  (int)Math.abs(r.nextGaussian() * 450  + 300);
      else if (m0 < 0.9)
        ret = (int)Math.abs(r.nextGaussian() * 1200 + 200);
      else
        ret = (int)Math.abs(r.nextGaussian() * 48000 + 3600);
    } while (ret >= limit);
    return ret;
  }
}
