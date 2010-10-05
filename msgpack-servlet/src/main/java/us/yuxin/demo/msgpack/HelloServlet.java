package us.yuxin.demo.msgpack;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(
		name = "HellServlet",
		value = "/hello")
public class HelloServlet extends HttpServlet {
	private static final long serialVersionUID = -6598627353024514611L;

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		resp.setContentType("text/html;Charset=utf8");
		PrintWriter writer = resp.getWriter();
		writer.println("<html><head><title>Hello World</title></head>");
		writer.println("<body><h1>Hi</h1></body></html>");
		writer.close();
	}
}
