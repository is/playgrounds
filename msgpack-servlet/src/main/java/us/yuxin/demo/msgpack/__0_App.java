package us.yuxin.demo.msgpack;

import org.msgpack.rpc.server.TCPServer;

public class __0_App {
	public int add(int a, int b) { return a + b; }
	
	public static void main(String[] args) {
		TCPServer s = new TCPServer("0.0.0.0", 1985, new __0_App());
		try {
			s.serv();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
