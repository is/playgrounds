import pika
import sys

from __cf import C

co = C.BC()
ch = co.channel()

ch.exchange_declare(exchange='direct_logs', exchange_type='direct')
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
ch.basic_publish(
  exchange='direct_logs', routing_key=severity, body=message)
print(' + Send %r:%r' % (severity, message))
co.close()
