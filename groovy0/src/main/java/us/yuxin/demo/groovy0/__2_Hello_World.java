package us.yuxin.demo.groovy0;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.core.util.StatusPrinter;

public class __2_Hello_World {
	public static void main(String[] args) {
		Logger logger = LoggerFactory.getLogger("us.yuxin.demo.groovy0.__2_Hello_World");
		logger.debug("Hello world.");
		
		LoggerContext lc = (LoggerContext)LoggerFactory.getILoggerFactory();
		StatusPrinter.print(lc);
	}
}
