package us.yuxin.demo.deploy.hello;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(
	name = "HelloServlet",
	value = "/hello")
public class HelloServlet extends HttpServlet {
	private static final long serialVersionID = 5833408168506211887L;

	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
		throws IOException, ServletException {
		resp.setStatus(200);
		PrintWriter w = resp.getWriter();
		w.println("Hello world.");
		w.close();
	}
}
