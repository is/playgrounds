import pika
import sys

from __cf import C

co = C.BC()
ch = co.channel()
ch.exchange_declare(exchange='direct_logs', exchange_type='direct')
r = ch.queue_declare('', exclusive=True)
qname = r.method.queue

severities = sys.argv[1:]
if not severities:
  sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
  sys.exit(1)

for serverity in severities:
  ch.queue_bind(exchange='direct_logs', queue=qname, routing_key=serverity)
print(' + waiting for logs. to exit press CTRL+c')

def callback(ch, method, properties, body):
  print(' - %r' % body)

ch.basic_consume(
  queue=qname, on_message_callback=callback, auto_ack=True)

ch.start_consuming()
