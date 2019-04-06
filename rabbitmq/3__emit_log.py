import pika
import sys

from __cf import C

co = C.BC()
ch = co.channel()

ch.exchange_declare(exchange='logs', exchange_type='fanout')
msg = ' '.join(sys.argv[1:]) or "info: Hello World"
for i in range(100):
  ch.basic_publish(exchange='logs', routing_key='', body="%s %d" % (msg, i))
print(' + Send %r' % msg)
ch.close()

