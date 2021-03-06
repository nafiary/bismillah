#!/usr/bin/python
import pika
import sys
from threading import Thread
from uuid import UUID
from peewee import *
import subprocess
import json
import time
import telegram

database = MySQLDatabase('mydb', user='remote', password='password123!', host='10.151.36.101', port=3306)

class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
    id = UUIDField(primary_key=True)
    name = CharField()
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    role = CharField()

class Devices(BaseModel):
    id = UUIDField(primary_key=True)
    name = CharField()
    type = CharField()
    location = CharField()
    address = CharField()

class Services(BaseModel):
    id = UUIDField(primary_key=True)
    servicename = CharField()
    command = CharField()
    params = CharField()
    devices_id = ForeignKeyField(Devices, on_delete='CASCADE')

class Subscribe(BaseModel):
    users_id = ForeignKeyField(Users, on_delete='CASCADE')
    devices_id = ForeignKeyField(Devices, on_delete='CASCADE')

class Subscribeservice(BaseModel):
    users_id = ForeignKeyField(Users, on_delete='CASCADE')
    services_id = ForeignKeyField(Services, on_delete='CASCADE')

def rabbitMq(exchange, address):
    # deviceservice =  Services.select().join(Devices).where(Services.devices_id == exchange)
    # for service in deviceservice:
    #     print service.command
    try:
        deviceservice =  Services.select().join(Devices).where(Services.devices_id == exchange)
        serviceList = []
        for service in deviceservice:
            serviceList.append({
            'id' : str(service.id),
            'servicename' : service.servicename,
            'command': service.command,
            'nrperesult' : None,
            'deviceid' : str(exchange)
            })
    except Exception as e:
        serviceList = []
        for service in deviceservice:
            serviceList.append({
            'id' : None,
            'servicename' : None,
            'command': None,
            'nrperesult' : None,
            'deviceid' : str(exchange)
            })
    # for service in serviceList:
    #     print service
    #     print "/usr/local/nagios/libexec/check_nrpe "+"-H "+address+ " -c "+ service['command']

    try:
        for service in serviceList:
            print "halo"
            p = subprocess.Popen(["/usr/local/nagios/libexec/check_nrpe", "-H", address, "-c", service['command']], stdout=subprocess.PIPE)
            print "==============================="
            print "/usr/local/nagios/libexec/check_nrpe "+"-H "+address+ " -c "+ service['command']
            output, err = p.communicate()
            print output.split('-')[1]
            print "====="
            # print p.poll()
            # if not p.wait():
            service['nrperesult'] = output.split('-')[1]
            message = json.dumps(serviceList)
            # else:
            #     service['nrperesult'] = 'NRPE CRITICAL -Error while checking related OID'
            #     message = json.dumps(serviceList)
    except Exception as e:
        # pass

        for service in serviceList:
            service['nrperesult'] = 'NRPE CRITICAL - Error while checking related service'
            message = json.dumps(serviceList)

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('10.151.36.98', '5672', '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    try:
        channel.basic_publish(exchange=str(exchange),
                              routing_key='',
                              body=json.dumps({ 'msg' : message, 'sendtime' : time.time() }))
    except Exception as e:
        channel.exchange_declare(exchange=str(exchange),
                                 exchange_type='fanout')
        channel.basic_publish(exchange=str(exchange),
                              routing_key='',
                              body=json.dumps({ 'msg' : message, 'sendtime' : time.time() }))
    print(" [x] Sent %r" % message)
    connection.close()

if __name__ == '__main__':

    while True:
        devices = Devices.select().where(Devices.address != "10.151.36.109")
        deviceInfo = []
        for device in devices:
            deviceInfo.append({
             'id' : device.id,
             'address' : device.address
            })
        print deviceInfo
        # for info in deviceInfo:
        #     threadRMQ = Thread(target=rabbitMq, kwargs=dict(exchange=info['id'], address=info['address']))
        #     threadRMQ.start()
        #     #threadRMQ.join()
        # time.sleep(2)
