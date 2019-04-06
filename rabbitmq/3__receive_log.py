import pika
import sys

from __cf import C

co = C.BC()
ch = co.channel()
ch.exchange_declare(exchange='logs', exchange_type='fanout')
r = ch.queue_declare('', exclusive=True)
qname = r.method.queue
ch.queue_bind(exchange='logs', queue=qname)
print(' + waiting for logs. to exit press CTRL+c')

def callback(ch, method, properties, body):
  print(' - %r' % body)

ch.basic_consume(
  queue=qname, on_message_callback=callback, auto_ack=True)
ch.start_consuming()
