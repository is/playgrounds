from __cf import C

import sys
import pika

co_params = pika.URLParameters(C.url)
co = pika.BlockingConnection(co_params)
ch = co.channel()

ch.queue_declare(queue='task_queue', durable=True)
message = " ".join(sys.argv[1:]) or "Hello World"
ch.basic_publish(
  exchange='',
  routing_key='task_queue',
  body=message,
  properties=pika.BasicProperties(delivery_mode=2)
  )
print(" - sent %r" % message)
co.close()
