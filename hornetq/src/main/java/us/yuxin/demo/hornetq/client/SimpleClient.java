package us.yuxin.demo.hornetq.client;

import java.util.HashMap;
import java.util.Map;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.MessageConsumer;
import javax.jms.MessageProducer;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;

import org.hornetq.api.core.TransportConfiguration;
import org.hornetq.api.jms.HornetQJMSClient;
import org.hornetq.core.remoting.impl.netty.NettyConnectorFactory;

public class SimpleClient {
	public static void main(String[] args) throws Exception {
		Connection connection = null;
		try {
			Queue queue = HornetQJMSClient.createQueue("ExampleQueue");
			Map<String, Object> connectionParams = new HashMap<String, Object>();
			connectionParams
					.put(
							org.hornetq.core.remoting.impl.netty.TransportConstants.PORT_PROP_NAME,
							5445);
			TransportConfiguration transportConfiguration = new TransportConfiguration(
					NettyConnectorFactory.class.getName(), connectionParams);
			ConnectionFactory cf = HornetQJMSClient
					.createConnectionFactory(transportConfiguration);
			
			connection = cf.createConnection();
			Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			MessageProducer producer = session.createProducer(queue);
			TextMessage message = session.createTextMessage("This is a text message");
			producer.send(message);
			MessageConsumer messageConsumer = session.createConsumer(queue);
			connection.start();
			TextMessage messageReceived = (TextMessage)messageConsumer.receive(5000);
			System.out.println("Received message: " + messageReceived.getText());
		} finally {
			if (connection != null) {
				connection.close();
			}
		}
	}
}
