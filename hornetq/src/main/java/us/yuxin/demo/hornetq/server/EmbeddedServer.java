package us.yuxin.demo.hornetq.server;

import org.hornetq.core.config.impl.FileConfiguration;
import org.hornetq.core.server.HornetQServer;
import org.hornetq.core.server.HornetQServers;
import org.hornetq.jms.server.JMSServerManager;
import org.hornetq.jms.server.impl.JMSServerManagerImpl;

// http://hornetq.blogspot.com/2009/09/hornetq-simple-example-using-maven.html
public class EmbeddedServer {
	public static void main(String[] args) {
		try {
			FileConfiguration configuration = new FileConfiguration();
			configuration.setConfigurationUrl("hornetq-configuration.xml");
			configuration.start();
			
			HornetQServer server = HornetQServers.newHornetQServer(configuration);
			JMSServerManager jmsServerManager = new JMSServerManagerImpl(server, "hornetq-jms.xml");
			jmsServerManager.setContext(null);
			jmsServerManager.start();			
		} catch (Throwable e) {
			System.out.println("FAILED::");
			e.printStackTrace();
		}
	}
}
