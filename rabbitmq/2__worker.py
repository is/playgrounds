from __cf import C

import pika
import time

co = C.BC()
ch = co.channel()
ch.queue_declare(queue="task_queue", durable=True)
print(" + waiting for message. exit press CTRL+C")

def cb(ch, method, properties, body):
  print( " - received %r" % body)
  time.sleep(body.count(b'.'))
  print( " - done")
  ch.basic_ack(delivery_tag=method.delivery_tag)

ch.basic_qos(prefetch_count=1)
ch.basic_consume(queue="task_queue",
  on_message_callback=cb)
ch.start_consuming()

