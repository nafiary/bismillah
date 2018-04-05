from flask import Flask, render_template
from flask_socketio import SocketIO, Namespace, emit
import logging
import pika
from threading import Thread

logging.basicConfig(level=logging.INFO)
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
logging.info('Connected: RabbitMQ Server')

clients = []

def disconnect_to_rabbitmq():
	channel.stop_consuming()
	connection.close()
	logging.info('Disconnected from Rabbitmq')

def consumer_callback(ch, method, properties, body):
		logging.info("[x] Received %r" % (body,))
		# The messagge is brodcast to the connected clients
		for itm in clients:
			itm.write_message(body)

class WebSocketHandler(Namespace):
    threadRMQ = None
    channel = connection.channel()

    def handle_message(self, message):
        print('received message: ' + str(message))

    def handle_json(self, json):
        print('received json: ' + str(json))

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

    def on_connect(self):
        self.threadRMQ = Thread(target=self.threaded_rmq)
        self.threadRMQ.start()
        logging.info('WebSocket opened')
        clients.append(self)

    def on_disconnect(self):
        print "status: "+ str(self.threadRMQ.isAlive())
        self.channel.stop_consuming()
        self.threadRMQ.join()
        print "status: "+ str(self.threadRMQ.isAlive())
        logging.info('WebSocket closed')
        clients.remove(self)

    # def on_my_event(self, data):
    #     emit('my_response', data)

socketio.on_namespace(WebSocketHandler('/ws'))

@app.route('/')
def index():
    return render_template('devicelist.html')

if __name__ == '__main__':
    logging.info('Server Starts')
    socketio.run(app, port=8000, host='0.0.0.0')
