#!/usr/bin/env python
import pika
import uuid
import json
import time
from multiprocessing import Process, Lock

def subscribe(queue_name):
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('10.151.36.98', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='8866b708-65da-4392-9774-4388c184ca7b',
                             exchange_type='fanout')

    result = channel.queue_declare(exclusive=True, queue=queue_name)
    # queue_name = result.method.queue

    channel.queue_bind(exchange='8866b708-65da-4392-9774-4388c184ca7b',
                       queue=queue_name)

    # print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        x = json.loads(body)
        # diffTime = time.time()-x['sendtime']
        # with open('hasiltesting/pubsubtest.csv', 'a') as f:
        #     f.write(diffTime+"\n")
        print(" [x] %r" % x)

        # print proc_num

    #lock.acquire()
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()
    # lock.release()

if __name__ == '__main__':
    while True:
        p = Process(target=subscribe, args=(str(uuid.uuid4()),))
        p.start()
        time.sleep(1)
