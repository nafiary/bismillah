#!/usr/bin/python
import pika
import sys
from multiprocessing import Process
from uuid import UUID
from peewee import *
import subprocess
import json
import time

database = MySQLDatabase('sysmondb', user='remote', password='password123!', host='10.151.36.101', port=3306)

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

class Oid(BaseModel):
    id = UUIDField(primary_key=True)
    oid = CharField()
    oidname = CharField()
    devices_id = ForeignKeyField(Devices, on_delete='CASCADE')

class Subscribe(BaseModel):
    users_id = ForeignKeyField(Users, on_delete='CASCADE')
    devices_id = ForeignKeyField(Devices, on_delete='CASCADE')

def rabbitMq(exchange, address):
    try:
        deviceoid =  Oid.select().join(Devices).where(Oid.devices_id == exchange)
        oidList = []
        for oid in deviceoid:
            oidList.append({
            'id' : str(oid.id),
            'oidname' : oid.oidname,
            'oid': oid.oid,
            'snmpresult' : None,
            'deviceid' : str(exchange)
            })
    except Exception as e:
        oidList = []
        for oid in deviceoid:
            oidList.append({
            'id' : None,
            'oidname' : None,
            'oid': None,
            'snmpresult' : None,
            'deviceid' : str(exchange)
            })

    try:
        for oid in oidList:
            p = subprocess.Popen(["/usr/local/nagios/libexec/check_snmp", "-H", address, "-o", oid['oid'], "-t", "1"], stdout=subprocess.PIPE)
            output, err = p.communicate()
            if not p.wait():
                oid['snmpresult'] = output.split('|')[0]
                message = json.dumps(oidList)
            else:
                oid['snmpresult'] = 'SNMP CRITICAL -Error while checking related OID'
                message = json.dumps(oidList)
    except Exception as e:
        for oid in oidList:
            oid['snmpresult'] = 'SNMP CRITICAL - Error while checking related OID'
            message = json.dumps(oidList)

    # print json.dumps({ 'msg' : message, 'sendtime' : time.time() })
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('10.151.36.70', 5672, '/', credentials)
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
        devices = Devices.select()
        deviceInfo = []
        for device in devices:
            deviceInfo.append({
             'id' : device.id,
             'address' : device.address
            })
        print deviceInfo
        for info in deviceInfo:
            threadRMQ = Process(target=rabbitMq, kwargs=dict(exchange=info['id'], address=info['address']))
            threadRMQ.start()
            threadRMQ.join()
	time.sleep(1)
