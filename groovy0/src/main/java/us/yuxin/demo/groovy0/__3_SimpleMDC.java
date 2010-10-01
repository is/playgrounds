package us.yuxin.demo.groovy0;

import java.net.URL;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.joran.JoranConfigurator;
import ch.qos.logback.core.joran.JoranConfiguratorBase;
import ch.qos.logback.core.joran.spi.JoranException;
import ch.qos.logback.core.util.Loader;
import ch.qos.logback.core.util.StatusPrinter;

public class __3_SimpleMDC {
	public static void main(String[] args) throws Exception {
		MDC.put("first", "Dorothy");
		configureViaXML_File();
		Logger logger = LoggerFactory.getLogger(__3_SimpleMDC.class);
		MDC.put("last", "Parker");
		
		logger.info("Check enclosed.");
		logger.debug("The mose beautiful two words in English.");
		
		MDC.put("first", "Richard");
		MDC.put("last", "Nixon");
		
		logger.info("I am not a crook.");
		logger.info("Attributed to the former US president. 17 Nov 1973.");
		
		// LoggerContext lc = (LoggerContext)LoggerFactory.getILoggerFactory();
		// StatusPrinter.print(lc);
	}
	
	
  static void configureViaXML_File() {
    LoggerContext lc = (LoggerContext) LoggerFactory.getILoggerFactory();
    try {
      JoranConfiguratorBase configurator = new JoranConfigurator();
      configurator.setContext(lc);
      lc.stop();
      URL url = Loader.getResourceBySelfClassLoader("us/yuxin/demo/groovy0/__3_SimpleMDC.xml");
      configurator.doConfigure(url);
    } catch (JoranException je) {
      StatusPrinter.print(lc);
    }
  }

}
