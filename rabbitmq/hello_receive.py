from __cf import C
import pika


def callback(ch, method, properties, body):
  print(" [x] receive %r" % body)

parameters = pika.URLParameters(C['url'])
co = pika.BlockingConnection(parameters)
channel = co.channel()
channel.basic_consume(
  queue='hello', auto_ack=True, on_message_callback=callback)
print(" [x] Waiting for messages. To exit press CTRL-C")
channel.start_consuming()
