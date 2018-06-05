#!/usr/bin/env python
import pika
import uuid
import json
import time
from multiprocessing import Process, Lock

def subscribe(queue_name, proc_num, lock):
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('10.151.36.70', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='logs',
                             exchange_type='fanout')

    result = channel.queue_declare(exclusive=True, queue=queue_name)
    # queue_name = result.method.queue

    channel.queue_bind(exchange='3db4a9fc-54a2-4771-bfd2-da7882d6b5c9',
                       queue=queue_name)

    # print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        x = json.loads(body)
        diffTime = time.time()-x['sendtime']
        # with open('hasiltesting/pubsubtest.csv', 'a') as f:
        #     f.write(diffTime+"\n")
        # print(" [x] %r" % diffTime)

        print proc_num

    lock.acquire()
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()
    lock.release()

if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        p = Process(target=subscribe, args=(str(uuid.uuid4()), str(i+1), lock))
        p.start()
