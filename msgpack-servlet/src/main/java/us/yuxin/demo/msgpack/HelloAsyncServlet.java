package us.yuxin.demo.msgpack;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;

import javax.servlet.AsyncContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(
	name = "HelloAsyncServliet", 
	value = "/ha",
	asyncSupported = true)
public class HelloAsyncServlet extends HttpServlet {
	private static final long serialVersionUID = 5688682285483101233L;
	public static class Executor implements Runnable {
		private AsyncContext ctx;
		public Executor(AsyncContext ctx) {
			this.ctx = ctx;
		}
		public void run() {
			try {
				Thread.sleep(10000);
				PrintWriter out = ctx.getResponse().getWriter();
				out.println("Finished at:" + new Date() + ".");
				out.flush();
				ctx.complete();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
	
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
		throws ServletException, IOException {
		resp.setContentType("text/html;charset=UTF-8");

		AsyncContext ctx = req.startAsync();
		new Thread(new Executor(ctx)).start();
		
		PrintWriter out = resp.getWriter();
		out.println("Enter servlet time:" + new Date() + ".");
		out.flush();
	}
}