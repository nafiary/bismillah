#!/usr/bin/env python

# How to send an web socket message using http://www.tornadoweb.org/.
# to get ready you have to install pika and tornado
# 1. pip install pika
# 2. pip install tornado

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import pika
from threading import Thread
import logging
logging.basicConfig(level=logging.INFO)

# web socket clients connected.
clients = []

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.151.36.98'))
logging.info('Connected: RabbitMQ Server')
# channel = connection.channel()

# def threaded_rmq():
# 	channel.queue_declare(queue="my_queue")
# 	logging.info('consumer ready, on my_queue')
# 	channel.basic_consume(consumer_callback, queue="my_queue", no_ack=True)
# 	channel.start_consuming()

def disconnect_to_rabbitmq():
	channel.stop_consuming()
	connection.close()
	logging.info('Disconnected from Rabbitmq')

def consumer_callback(ch, method, properties, body):
		logging.info("[x] Received %r" % (body,))
		# The messagge is brodcast to the connected clients
		for itm in clients:
			itm.write_message(body)

class SocketHandler(tornado.websocket.WebSocketHandler):
	threadRMQ = None
	channel = connection.channel()

	def threaded_rmq(self):
		self.channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
		result = self.channel.queue_declare(exclusive=True)
		queue_name = result.method.queue

		self.channel.queue_bind(exchange='logs',
		                   queue=queue_name)
		logging.info('consumer ready, on my_queue')
		self.channel.basic_consume(consumer_callback, queue=queue_name, no_ack=True)
		self.channel.start_consuming()

	def open(self):
		self.threadRMQ = Thread(target=self.threaded_rmq)
		self.threadRMQ.start()
		logging.info('WebSocket opened')
		clients.append(self)

	def on_close(self):
		print "status: "+ str(self.threadRMQ.isAlive())
		self.channel.stop_consuming()
		self.threadRMQ.join()
		print "status: "+ str(self.threadRMQ.isAlive())
		logging.info('WebSocket closed')
		clients.remove(self)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("websocket.html")


application = tornado.web.Application([
    (r'/ws', SocketHandler),
    (r"/", MainHandler),
])

def startTornado():
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

def stopTornado():
    tornado.ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
	logging.info('Starting thread RabbitMQ')
	# threadRMQ = Thread(target=threaded_rmq)
	# threadRMQ.start()

   	logging.info('Starting thread Tornado')

   	threadTornado = Thread(target=startTornado)
   	threadTornado.start()
	try:
		raw_input("Server ready. Press enter to stop\n")
	except SyntaxError:
		pass
	try:
		logging.info('Disconnecting from RabbitMQ..')
		disconnect_to_rabbitmq()
	except Exception, e:
		pass
	stopTornado();

	logging.info('See you...')
