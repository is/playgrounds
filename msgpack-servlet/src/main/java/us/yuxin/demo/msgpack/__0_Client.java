package us.yuxin.demo.msgpack;

import org.msgpack.rpc.client.EventLoop;
import org.msgpack.rpc.client.TCPClient;

public class __0_Client {
	public static void main(String[] args) {
		EventLoop loop = new EventLoop();
		TCPClient c = new TCPClient("localhost", 1985, loop);
		try {
			int result = ((Number)c.call("add", new Object[] {new Integer(10), new Integer(30)})).intValue();
			System.out.println("result:" + result);
		} catch (Exception e) {
			e.printStackTrace();
		}
		c.close();
		loop.shutdown();
	}
}
