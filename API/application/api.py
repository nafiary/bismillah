import datetime

from flask import Flask
from flask import g
from flask import redirect
from flask import request
from flask import session, jsonify
from flask import url_for, abort, render_template, flash
from functools import wraps
from hashlib import md5
from peewee import *
import uuid
# from playhouse.shortcuts import *
from flask import Flask, jsonify, request
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims, get_raw_jwt
)


DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=12)
jwt = JWTManager(app)

blacklist = set()

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

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user.role,
    'email': user.email,
    'username': user.username,
    'name': user.name}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
@jwt_required
def homepage():
    ret = jsonify({
        'current_identity': get_jwt_identity(),
        'current_username': get_jwt_claims()['username'],
        'current_email': get_jwt_claims()['email'],
        'current_role': get_jwt_claims()['role'],
        'current_name': get_jwt_claims()['name']
    })
    return ret, 200


@app.route('/register', methods=['GET', 'POST'])
def join():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                user = Users.create(
                    id=uuid.uuid4(),
                    name=request.json.get('name', None),
                    username=request.json.get('username', None),
                    password=md5((request.json.get('password', None)).encode('utf-8')).hexdigest(),
                    email=request.json.get('email', None),
                    join_date=datetime.datetime.now())

            return jsonify({"msg": "New User Created"}), 200

        except Exception as e:
            print e
            return jsonify({"msg": "Error Create New User"}), 401

    return homepage()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        try:
            pw_hash = md5(password.encode('utf-8')).hexdigest()
            user = Users.get(
                (Users.username == username) &
                (Users.password == pw_hash))
        except Exception as e:
            return jsonify({"msg": "Bad username or password"}), 401
        else:
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token), 200

    res = jsonify({
        'status': 'not logged in',
        })
    res.status_code = 200
    return res

@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

@app.route('/users', methods=['GET'])
@jwt_required
def users():
    if request.method == 'GET':
        try:
            userlist = []
            users = Users.select().order_by(Users.username)
            for user in users:
                data = userlist.append({
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'username': user.username,
                    'role': user.role,
                    })
            res = jsonify(userlist)
            res.status_code = 200
        except Exception as e:
            # if no results are found.
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

@app.route('/users/<string:username>', methods=['GET'])
@jwt_required
def user_detail(username):
    # users = Users.select().where(Users.username == username).get()
    # usersdevice = Users.select(Subscribe.users_id, Subscribe.devices_id).join(Subscribe).join(Devices).where(Users.id == users.id)
    # try:
    #     print usersdevice[0].subscribe.users_id.id
    # except Exception as e:
    #     print e
    # return jsonify({ 'msg' : 'testing' })
    if request.method == 'GET':
        try:
            users = Users.select().where(Users.username == username).get()
            usersdevice = Users.select(Subscribe.users_id, Subscribe.devices_id).join(Subscribe).join(Devices).where(Users.id == users.id)
            usersservice = Users.select(Subscribeservice.users_id, Subscribeservice.services_id).join(Subscribeservice).join(Services).where(Users.id == users.id)
            dicti =  {
                    'id': usersdevice[0].subscribe.users_id.id,
                    'name': usersdevice[0].subscribe.users_id.name,
                    'username': usersdevice[0].subscribe.users_id.username,
                    'email': usersdevice[0].subscribe.users_id.email,
                    'role': usersdevice[0].subscribe.users_id.role,
                    'subscribing' : [],
                    'subscribingservice' : [],
                    }
            for item in usersdevice:
                dicti['subscribing'].append({
                'id' : item.subscribe.devices_id.id,
                'name' : item.subscribe.devices_id.name,
                'type' : item.subscribe.devices_id.type,
                })
            for item in usersservice:
                dicti['subscribingservice'].append({
                'id' : item.subscribeservice.services_id.id,
                'servicename' : item.subscribeservice.services_id.servicename,
                'command' : item.subscribeservice.services_id.command,
                'params' : item.subscribeservice.services_id.params,
                'deviceid' : item.subscribeservice.services_id.devices_id.id,
                })
            res = jsonify(dicti)
            # print dicti
            res.status_code = 200
        except Exception as e:
            print e
            try:
                users = Users.select().where(Users.username == username).get()
                res = jsonify({
                    'id': users.id,
                    'name': users.name,
                    'username': users.username,
                    'email': users.email,
                    'role': users.role,
                    'subscribing' : None,
                    'subscribingservice' : None,
                    })
                res.status_code = 200
            except Devices.DoesNotExist:
                output = {
                    "error": "No results found. Check url again",
                    "url": request.url,
                }
                res = jsonify(output)
                res.status_code = 404
        return res

@app.route('/devices/create', methods=['POST'])
@jwt_required
def createdevice():
    if request.method == 'POST' and request.is_json:
        try:
            uuiddevices = uuid.uuid4()
            with database.atomic() as createdevice:
                Devices.create(
                    id=uuiddevices,
                    name=request.json.get('name', None),
                    type=request.json.get('type', None),
                    location=request.json.get('location', None),
                    address=request.json.get('address', None),)
            try:
                for value in request.json.get('service', None):
                    with database.atomic() as createservice:
                        Services.create(
                            id=uuid.uuid4(),
                            servicename=value['servicename'],
                            command=value['command'],
                            params=value['params'],
                            devices_id=uuiddevices,)

            except Exception as e:
                createdevice.rollback()
                return jsonify({"msg": "Error while creating OID data"}), 401

            res = jsonify({"msg": "Device data created", "deviceid" : uuiddevices}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while creating device data"}), 401
    return res

@app.route('/devices/edit/<string:id>', methods=['POST'])
@jwt_required
def editdevice(id):
    if request.method == 'POST' and request.is_json:
        try:
            edit = Devices.update(
                    name=request.json.get('name', None),
                    type=request.json.get('type', None),
                    location=request.json.get('location', None),
                    address=request.json.get('address', None)).where(Devices.id==id)
            edit.execute()
            res = jsonify({"msg": "Device data edited"}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while creating device data"}), 401
    return res


@app.route('/devices/delete', methods=['DELETE'])
@jwt_required
def deletedevices():
    if request.method == 'DELETE' and request.is_json == True:
        try:
            with database.atomic():
                devices = Devices.delete().where( Devices.id == request.json.get('deviceid', None) )
                devices.execute()
            res = jsonify({"msg": "Device Deleted"}), 200

        except Exception as e:
            print e
            res = jsonify({"msg": "Error while deteting device"}), 401

    return res

@app.route('/devices', methods=['GET'])
@jwt_required
def devices():
    if request.method == 'GET':
        try:
            devicelist = []
            devices = Devices.select().order_by(Devices.name)
            for device in devices:
                data = devicelist.append({
                    'id': device.id,
                    'name': device.name,
                    'type': device.type,
                    'location': device.location,
                    'address': device.address,
                    })
            res = jsonify(devicelist)
            res.status_code = 200
        except Exception as e:
            # if no results are found.
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

@app.route('/devices/<string:id>', methods=['GET'])
@jwt_required
def device_detail(id):
    # device = Devices.select(Subscribe.users_id, Subscribe.devices_id).join(Subscribe).join(Users).where(Devices.id == id)
    # oid = Oid.select(Subscribeoid.users_id, Subscribeoid.oid_id).join(Subscribeoid).join(Users).where(Subscribeoid.oid_id.devices_id == id)
    # deviceoid =  Oid.select().join(Devices).where(Oid.devices_id == id)
    # print oid[0].subscribeoid.oid_id.id
    # return jsonify({ 'msg' : 'test' })
    if request.method == 'GET':
        try:
            device = Devices.select(Subscribe.users_id, Subscribe.devices_id).join(Subscribe).join(Users).where(Devices.id == id)
            service = Services.select(Subscribeservice.users_id, Subscribeservice.services_id).join(Subscribeservice).join(Users).where(Subscribeservice.services_id.devices_id == id)
            deviceservice =  Services.select().join(Devices).where(Services.devices_id == id)

            try:
                #coba ada yang subscribe ga
                dicti =  {
                        'id': device[0].subscribe.devices_id.id,
                        'name': device[0].subscribe.devices_id.name,
                        'type': device[0].subscribe.devices_id.type,
                        'location': device[0].subscribe.devices_id.location,
                        'address': device[0].subscribe.devices_id.address,
                        'subscribed_by' : [],
                        'service' : [],
                        }
                for item in device:
                    dicti['subscribed_by'].append({
                    'id' : item.subscribe.users_id.id,
                    'username' : item.subscribe.users_id.username,
                    })
                for item in deviceservice:
                    dicti['service'].append({
                    'id' : item.id,
                    'servicename' : item.servicename,
                    'command' : item.command,
                    'params' : item.params,
                    'subscribed_by' : []
                    })

                try:
                    for index, item in enumerate(service):
                        for item2 in dicti['service']:
                            if item2['id'] == item.subscribeservice.services_id.id:
                                item2['subscribed_by'].append({
                                'id' : item.subscribeservice.users_id.id,
                                'email' : item.subscribeservice.users_id.email,
                                'name' : item.subscribeservice.users_id.name,
                                'username' : item.subscribeservice.users_id.username,
                                'password' : item.subscribeservice.users_id.password,
                                'role' : item.subscribeservice.users_id.role,
                                })
                except Exception as e:
                    pass

                res = jsonify(dicti)
                res.status_code = 200
            except Exception as e:
                print e
                #kalo ga ada yang subscribe dibikin none subscribed_by nya
                dicti =  {
                        'id': deviceservice[0].devices_id.id,
                        'name': deviceservice[0].devices_id.name,
                        'type': deviceservice[0].devices_id.type,
                        'location': deviceservice[0].devices_id.location,
                        'address': deviceservice[0].devices_id.address,
                        'subscribed_by' : None,
                        'service' : [],
                        }
                for item in deviceservice:
                    dicti['service'].append({
                    'id' : item.id,
                    'servicename' : item.servicename,
                    'command' : item.command,
                    'params' : item.params,
                    'subscribed_by' : []
                    })
                res = jsonify(dicti)
                res.status_code = 200

        except Exception as e:
            try:
                device = Devices.select().where(Devices.id == id).get()
                res = jsonify({
                    'id': device.id,
                    'name': device.name,
                    'type': device.type,
                    'location': device.location,
                    'address': device.address,
                    'subscribed_by' : None,
                    'service' : None,
                    })
                res.status_code = 200
            except Exception as e:
                output = {
                    "error": "No results found. Check url again",
                    "url": request.url,
                }
                res = jsonify(output)
                res.status_code = 404
        return res

@app.route('/service/create', methods=['POST'])
@jwt_required
def createservice():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                createservice = Services.create(
                    id=uuid.uuid4(),
                    servicename=request.json.get('servicename', None),
                    command=request.json.get('command', None),
                    params=request.json.get('params', None),
                    devices_id=request.json.get('device_id', None),)

            res =  jsonify({"msg": "Service data created"}), 200

        except Exception as e:
            print e
            res = jsonify({"msg": "Error while creating service data"}), 401

    return res

@app.route('/service/edit', methods=['POST'])
@jwt_required
def editservice():
    if request.method == 'POST' and request.is_json:
        try:
            # print request.json.get('id', None)
            with database.atomic():
                editservice = Services.update(
                    servicename=request.json.get('servicename', None),
                    command=request.json.get('command', None),).where(Services.id == request.json.get('services_id', None))
                editservice.execute()

            res = jsonify({"msg": "Service data edited"}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while edit service data"}), 401

    return res

@app.route('/service/delete', methods=['DELETE'])
@jwt_required
def deleteoid():
    if request.method == 'DELETE' and request.is_json == True:
        try:
            with database.atomic():
                deleteservice = Services.delete().where( Services.id == request.json.get('services_id', None) )
                deleteservice.execute()
            res = jsonify({"msg": "Service Deleted"}), 200

        except Exception as e:
            print e
            res = jsonify({"msg": "Error while deleting service"}), 401

    return res

@app.route('/subscribe/devices', methods=['POST'])
@jwt_required
def subscribedevice():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                subscribe = Subscribe.create(
                    users_id=get_jwt_identity(),
                    devices_id=request.json.get('deviceid', None),)

            res = jsonify({"msg": "Device Subscribed"}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while subscribing devices"}), 401

    return res

@app.route('/unsubscribe/devices', methods=['POST'])
@jwt_required
def unsubscribedevice():
    if request.method == 'POST' and request.is_json == True:
        try:
            with database.atomic():
                unsubscribe = Subscribe.delete().where( Subscribe.users_id == get_jwt_identity(), Subscribe.devices_id == request.json.get('deviceid', None) )
                unsubscribe.execute()
            res = jsonify({"msg": "Device Unsubscribed"}), 200

        except Exception as e:
            res = ({"msg": "Error while unsubscribing device"}), 401

    return res

@app.route('/subscribe/service', methods=['POST'])
@jwt_required
def subscribeservice():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                subscribe = Subscribeservice.create(
                    users_id=get_jwt_identity(),
                    services_id=request.json.get('service_id', None),)

            res = jsonify({"msg": "Service Subscribed"}), 200

        except Exception as e:
            print e
            res = jsonify({"msg": "Error while subscribing services"}), 401

    return res

@app.route('/unsubscribe/service', methods=['POST'])
@jwt_required
def unsubscribeservice():
    if request.method == 'POST' and request.is_json == True:
        try:
            with database.atomic():
                unsubscribe = Subscribeservice.delete().where( Subscribeservice.users_id == get_jwt_identity(), Subscribeservice.services_id == request.json.get('service_id', None) )
                unsubscribe.execute()
            res = jsonify({"msg": "Service Unsubscribed"}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while unsubscribing Service"}), 401

    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
