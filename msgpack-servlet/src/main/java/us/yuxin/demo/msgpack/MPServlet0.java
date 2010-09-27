package us.yuxin.demo.msgpack;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.AbstractList;
import java.util.ArrayList;


import javax.servlet.ServletException;
import javax.servlet.ServletInputStream;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.msgpack.Packer;
import org.msgpack.Unpacker;

public class MPServlet0 extends HttpServlet {

	/**
	 * 
	 */
	private static final long serialVersionUID = 6067111471398491974L;

	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		int contentLength = req.getContentLength();
		Unpacker unpacker = new Unpacker();
		
		unpacker.reserveBuffer(contentLength);
		
		byte[] unpackBuffer = unpacker.getBuffer();
		ServletInputStream sis = req.getInputStream();
		
		int offset = 0;
		while (true) {
			int n = sis.read(unpackBuffer, offset, contentLength - offset);
			if (n < 0) {
				throw new ServletException("Malformed post data");
			}
			
			offset += n;
			if (offset == contentLength)
				break;
		}
		sis.close();
		unpacker.bufferConsumed(contentLength);
		AbstractList<?> request = (AbstractList<?>)unpacker.getData();
		
		ArrayList<Object> response = new ArrayList<Object>();
		
		response.add("MPServilet0");
		response.add(((Number)request.get(1)).intValue() * 4);
		ByteArrayOutputStream o = new ByteArrayOutputStream();
		Packer packer = new Packer(o);
		packer.pack(response);
		byte[] outputBuffer = o.toByteArray();
		
		resp.setStatus(200);
		resp.setContentType("application/x-msgpack");
		resp.setContentLength(outputBuffer.length);
		
		ServletOutputStream os = resp.getOutputStream();
		os.write(outputBuffer);
		os.close();
	}
}
