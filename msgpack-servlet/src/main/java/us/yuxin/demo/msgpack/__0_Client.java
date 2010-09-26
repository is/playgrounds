package us.yuxin.demo.msgpack;

import org.msgpack.rpc.client.EventLoop;
import org.msgpack.rpc.client.TCPClient;

public class __0_Client {
	public static void main(String[] args) {
		EventLoop loop = new EventLoop();
		TCPClient c = new TCPClient("localhost", 1985, loop);
		try {
			Object result = c.call("add", new Object[] {new Integer(100), new Integer(300)});
			System.out.println("result:" + result);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
