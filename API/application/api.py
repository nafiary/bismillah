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

database = MySQLDatabase('mydb', user='root', password='password123!', host='localhost', port=3316)

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

class Subscribeoid(BaseModel):
    users_id = ForeignKeyField(Users, on_delete='CASCADE')
    oid_id = ForeignKeyField(Oid, on_delete='CASCADE')

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user.role,
    'email': user.email,
    'username': user.username}

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
        'current_role': get_jwt_claims()['role']
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
            usersoid = Users.select(Subscribeoid.users_id, Subscribeoid.oid_id).join(Subscribeoid).join(Oid).where(Users.id == users.id)
            dicti =  {
                    'id': usersdevice[0].subscribe.users_id.id,
                    'name': usersdevice[0].subscribe.users_id.name,
                    'username': usersdevice[0].subscribe.users_id.username,
                    'email': usersdevice[0].subscribe.users_id.email,
                    'role': usersdevice[0].subscribe.users_id.role,
                    'subscribing' : [],
                    'subscribingoid' : [],
                    }
            for item in usersdevice:
                dicti['subscribing'].append({
                'id' : item.subscribe.devices_id.id,
                'name' : item.subscribe.devices_id.name,
                'type' : item.subscribe.devices_id.type,
                })
            for item in usersoid:
                dicti['subscribingoid'].append({
                'id' : item.subscribeoid.oid_id.id,
                'oidname' : item.subscribeoid.oid_id.oidname,
                'oid' : item.subscribeoid.oid_id.oid,
                'deviceid' : item.subscribeoid.oid_id.devices_id.id,
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
                    'subscribingoid' : None,
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
                for value in request.json.get('oid', None):
                    with database.atomic() as createoid:
                        Oid.create(
                            id=uuid.uuid4(),
                            oid=value['oid'],
                            oidname=value['oidname'],
                            devices_id=uuiddevices,)

            except Exception as e:
                createdevice.rollback()
                return jsonify({"msg": "Error while creating OID data"}), 401

            res = jsonify({"msg": "Device data created"}), 200

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
            oid = Oid.select(Subscribeoid.users_id, Subscribeoid.oid_id).join(Subscribeoid).join(Users).where(Subscribeoid.oid_id.devices_id == id)
            deviceoid =  Oid.select().join(Devices).where(Oid.devices_id == id)

            try:
                #coba ada yang subscribe ga
                dicti =  {
                        'id': device[0].subscribe.devices_id.id,
                        'name': device[0].subscribe.devices_id.name,
                        'type': device[0].subscribe.devices_id.type,
                        'location': device[0].subscribe.devices_id.location,
                        'address': device[0].subscribe.devices_id.address,
                        'subscribed_by' : [],
                        'oid' : [],
                        }
                for item in device:
                    dicti['subscribed_by'].append({
                    'id' : item.subscribe.users_id.id,
                    'username' : item.subscribe.users_id.username,
                    })
                for item in deviceoid:
                    dicti['oid'].append({
                    'id' : item.id,
                    'oid' : item.oid,
                    'oidname' : item.oidname,
                    'subscribed_by' : []
                    })

                try:
                    for index, item in enumerate(oid):
                        for item2 in dicti['oid']:
                            if item2['id'] == item.subscribeoid.oid_id.id:
                                item2['subscribed_by'].append({
                                'id' : item.subscribeoid.users_id.id,
                                'email' : item.subscribeoid.users_id.email,
                                'name' : item.subscribeoid.users_id.name,
                                'username' : item.subscribeoid.users_id.username,
                                'password' : item.subscribeoid.users_id.password,
                                'role' : item.subscribeoid.users_id.role,
                                })
                except Exception as e:
                    pass

                res = jsonify(dicti)
                res.status_code = 200
            except Exception as e:
                print e
                #kalo ga ada yang subscribe dibikin none subscribed_by nya
                dicti =  {
                        'id': deviceoid[0].devices_id.id,
                        'name': deviceoid[0].devices_id.name,
                        'type': deviceoid[0].devices_id.type,
                        'location': deviceoid[0].devices_id.location,
                        'address': deviceoid[0].devices_id.address,
                        'subscribed_by' : None,
                        'oid' : [],
                        }
                for item in deviceoid:
                    dicti['oid'].append({
                    'id' : item.id,
                    'oid' : item.oid,
                    'oidname' : item.oidname,
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
                    'oid' : None,
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

@app.route('/oid/create', methods=['POST'])
@jwt_required
def createoid():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                createoid = Oid.create(
                    id=uuid.uuid4(),
                    oid=request.json.get('oid', None),
                    oidname=request.json.get('oidname', None),
                    devices_id=request.json.get('deviceid', None),)

            res =  jsonify({"msg": "OID data created"}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while creating OID data"}), 401

    return res

@app.route('/oid/edit', methods=['POST'])
@jwt_required
def editoid():
    if request.method == 'POST' and request.is_json:
        try:
            # print request.json.get('id', None)
            with database.atomic():
                editoid = Oid.update(
                    oid=request.json.get('oid', None),
                    oidname=request.json.get('oidname', None),).where(Oid.id == request.json.get('id', None))
                editoid.execute()

            res = jsonify({"msg": "OID data edited"}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while edit OID data"}), 401

    return res

@app.route('/oid/delete', methods=['DELETE'])
@jwt_required
def deleteoid():
    if request.method == 'DELETE' and request.is_json == True:
        try:
            with database.atomic():
                deleteoid = Oid.delete().where( Oid.id == request.json.get('oid_id', None) )
                deleteoid.execute()
            res = jsonify({"msg": "Oid Deleted"}), 200

        except Exception as e:
            print e
            res = jsonify({"msg": "Error while deleting oid"}), 401

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

@app.route('/subscribe/oid', methods=['POST'])
@jwt_required
def subscribeoid():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                subscribe = Subscribeoid.create(
                    users_id=get_jwt_identity(),
                    oid_id=request.json.get('oid_id', None),)

            res = jsonify({"msg": "OID Subscribed"}), 200

        except Exception as e:
            print e
            res = jsonify({"msg": "Error while subscribing OID"}), 401

    return res

@app.route('/unsubscribe/oid', methods=['POST'])
@jwt_required
def unsubscribeoid():
    if request.method == 'POST' and request.is_json == True:
        try:
            with database.atomic():
                unsubscribe = Subscribeoid.delete().where( Subscribeoid.users_id == get_jwt_identity(), Subscribeoid.oid_id == request.json.get('oid_id', None) )
                unsubscribe.execute()
            res = jsonify({"msg": "OID Unsubscribed"}), 200

        except Exception as e:
            res = jsonify({"msg": "Error while unsubscribing OID"}), 401

    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
