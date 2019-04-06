from __cf import C

import pika
import time

parameters = pika.URLParameters(C['url'])
co = pika.BlockingConnection(parameters)
channel = co.channel()
channel.queue_declare(queue='hello')
for i in range(20):
  channel.basic_publish(exchange='',
    routing_key='hello',
    body='Hello World! %.2f' % time.time())
co.close()
