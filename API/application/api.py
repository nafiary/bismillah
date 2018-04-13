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
from pprint import pprint
from flask import Flask, jsonify, request
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

class Subscribe(BaseModel):
    users_id = ForeignKeyField(Users)
    devices_id = ForeignKeyField(Devices)

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

        except IntegrityError:
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
        except Users.DoesNotExist:
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

@app.route('/users/<string:username>', methods=['GET'])
@jwt_required
def user_detail(username):
    if request.method == 'GET':
        try:
            users = Users.select().where(Users.username == username).get()
            res = jsonify({
                'id': users.id,
                'name': users.name,
                'username': users.username,
                'password': users.password,
                'email': users.email,
                })
            res.status_code = 200
        except Users.DoesNotExist:
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

@app.route('/createdevice', methods=['GET', 'POST'])
@jwt_required
def createdevice():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                device = Devices.create(
                    id=uuid.uuid4(),
                    name=request.json.get('name', None),
                    type=request.json.get('type', None),)

            return jsonify({"msg": "Device data created"}), 200

        except IntegrityError:
            jsonify({"msg": "Error while creating device data"}), 401

    return homepage()

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
                    })
            res = jsonify(devicelist)
            res.status_code = 200
        except Devices.DoesNotExist:
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
    if request.method == 'GET':
        try:
            device = Devices.select().where(Devices.id == id).get()
            res = jsonify({
                'id': device.id,
                'name': device.name,
                'type': device.type,
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

@app.route('/subscribe', methods=['GET', 'POST'])
@jwt_required
def subscribe():
    if request.method == 'POST' and request.is_json:
        try:
            with database.atomic():
                subscribe = Subscribe.create(
                    users_id=get_jwt_identity(),
                    devices_id=request.json.get('deviceid', None),)

            return jsonify({"msg": "Device Subscribed"}), 200

        except IntegrityError:
            jsonify({"msg": "Error while subscribing devices"}), 401

    return homepage()

@app.route('/unsubscribe', methods=['GET', 'POST'])
@jwt_required
def unsubscribe():
    if request.method == 'POST' and request.is_json == True:
        try:
            with database.atomic():
                unsubscribe = Subscribe.delete().where( Subscribe.users_id == get_jwt_identity(), Subscribe.devices_id == request.json.get('deviceid', None) )
                unsubscribe.execute()
            return jsonify({"msg": "Device Unsubscribed"}), 200

        except IntegrityError:
            jsonify({"msg": "Error while unsubscribing device devices"}), 401

    return homepage()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
