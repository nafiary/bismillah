# #!/usr/bin/env python
#
# import pika
# import logging
# logging.basicConfig()
#
# connection = pika.BlockingConnection()
# print 'Connected:localhost'
# channel = connection.channel()
# channel.queue_declare(queue="my_queue")
# channel.basic_publish(exchange='',
#                       routing_key='my_queue',
#                       body='Test Message')
# connection.close()

#!/usr/bin/env python
import pika
import sys
import logging
logging.basicConfig()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.151.36.98'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()
