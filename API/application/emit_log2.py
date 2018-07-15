#!/usr/bin/python
import pika
import sys
from threading import Thread
from uuid import UUID
from peewee import *
import subprocess
import json
import time
import requests
import telegram
import datetime

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
    chat_id = IntegerField()

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
    laststatus = IntegerField()
    currstatus = IntegerField()

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
            'deviceid' : str(exchange),
            'laststatus' : service.laststatus,
            'currstatus' : service.currstatus
            })
    except Exception as e:
        serviceList = []
        for service in deviceservice:
            serviceList.append({
            'id' : None,
            'servicename' : None,
            'command': None,
            'nrperesult' : None,
            'deviceid' : str(exchange),
            'laststatus' : True,
            'currstatus' : True
            })
    # for service in serviceList:
    #     print service
    #     print "/usr/local/nagios/libexec/check_nrpe "+"-H "+address+ " -c "+ service['command']


    for service in serviceList:

        print "Hai =============================================================================\n"
        print service['servicename']
        print service['id']
        print "Hello =============================================================================\n"

        try:
            # for service in serviceList:
            p = subprocess.Popen(["/usr/local/nagios/libexec/check_nrpe", "-H", address, "-c", service['command']], stdout=subprocess.PIPE)
            # print "/usr/local/nagios/libexec/check_nrpe "+"-H "+address+ " -c "+ service['command']
            output, err = p.communicate()
            # print output.split('-')[1]
            # print p.poll()
            # if not p.wait():
            service['nrperesult'] = output.split('-')[1]
            message = json.dumps(serviceList)

            print "nyala"

            service['laststatus'] = 1

            query1 = Services.select().where(Services.id == service['id']).first()
            query1.laststatus = service['laststatus']
            
            try:
                query1.save()    
            except Exception as e:
                raise e


            service['currstatus'] = 1
            query1 = Services.select().where(Services.id == service['id']).first()
            query1.currstatus = service['currstatus']
            
            try:
                query1.save()    
            except Exception as e:
                raise e

            # else:
            #     service['nrperesult'] = 'NRPE CRITICAL -Error while checking related OID'
            #     message = json.dumps(serviceList)
        except Exception as e:
            
            service['currstatus'] = 0

            query1 = Services.select().where(Services.id == service['id']).first()
            query1.currstatus = service['currstatus']
            
            try:
                query1.save()    
            except Exception as e:
                raise e


            # query3 = Services.update(currstatus=service['currstatus']).where(Services.id == service['id'])
            # query3.execute()
            # for service in serviceList:
            service['nrperesult'] = 'NRPE CRITICAL - Error while checking related service'
            message = json.dumps(serviceList)


            if int(service['laststatus']) != int(service['currstatus']):

                service['laststatus'] = 0

                query1 = Services.select().where(Services.id == service['id']).first()
                query1.laststatus = service['laststatus']
                
                try:
                    query1.save()
                except Exception as e:
                    raise e

                try:
                    login = requests.post('http://10.151.36.33:5000/login', json={"username":"afifridho", "password":"afifridho"}).json()
                    accesstoken =  login["access_token"]
                except Exception as e:
                    raise e
                headers = { 'Authorization' : 'Bearer %s' % accesstoken }
                devicedetail = requests.get('http://10.151.36.33:5000/devices/%s' % exchange, headers = headers).json()

                for i in devicedetail["service"]:
                    if service["id"] == i["id"]:
                        for j in i["subscribed_by"]:

                            try:
                                if j["username"]=="nafia":
                                    continue
                                print "lanjut"
                                bot = telegram.Bot(token='611181819:AAGuGafaEg5W0_iTYQ5OxOZBz_JEeJPqGbQ')
                                bot.sendMessage(chat_id=j["chat_id"], text=str(datetime.datetime.now())+" disconnected :(")
                            
                            except Exception as e:
                                raise e

                       

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
    # print(" [x] Sent %r" % message)
    connection.close()
    print "selesai"

if __name__ == '__main__':

    while True:
        devices = Devices.select().where(Devices.address != "10.151.36.109")
        deviceInfo = []
        for device in devices:
            deviceInfo.append({
             'id' : device.id,
             'address' : device.address
            })
        #
        # print deviceInfo
        for info in deviceInfo:

            try:
                threadRMQ = Thread(target=rabbitMq, kwargs=dict(exchange=info['id'], address=info['address']))
                threadRMQ.start()
            except Exception as e:
                raise e

            
            #threadRMQ.join()
        time.sleep(2)
