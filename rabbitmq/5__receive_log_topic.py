import pika
import sys

from __cf import C

co = C.BC()
ch = co.channel()
ch.exchange_declare(exchange='topic_logs', exchange_type='topic')
r = ch.queue_declare('', exclusive=True)
queue_name = r.method.queue
binding_keys = sys.argv[1:]

if not binding_keys:
  sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
  sys.exit(1)

for binding_key in binding_keys:
  ch.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

def callback(ch, method, properties, body):
  print(' - %r' % body)

ch.basic_consume(
  queue=queue_name, on_message_callback=callback, auto_ack=True)

ch.start_consuming()
