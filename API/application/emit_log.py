#!/usr/bin/python
import pika
import sys
import MySQLdb
from threading import Thread
from uuid import UUID

def rabbitMq(exchange):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    message = ' '.join(sys.argv[1:]) or str(exchange)
    channel.basic_publish(exchange=str(exchange),
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)
    channel.queue_delete(queue='hello')
    connection.close()

if __name__ == '__main__':
    db = MySQLdb.connect(host="localhost",
                         user="afifridho",
                         passwd="afifridho",
                         db="mydb")

    cur = db.cursor()

    cur.execute("select distinct devices.* from devices join subscribe on subscribe.devices_id = devices.id join users on subscribe.users_id = users.id ")

    deviceid = []
    for row in cur.fetchall():
        deviceid.append(UUID(row[0]))

    db.close()

    for id in deviceid:
        threadRMQ = Thread(target=rabbitMq, kwargs=dict(exchange=id))
        threadRMQ.start()
