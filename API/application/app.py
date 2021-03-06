import datetime

from flask import Flask
from flask import g
from flask import redirect
from flask import request
from flask import session, jsonify
from flask import url_for, abort, render_template, flash
from functools import wraps
from hashlib import md5
import uuid
import requests
from datetime import timedelta
import json

from flask_assets import Environment, Bundle

DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
# assets = Environment(app)

# js = Bundle('js/jquery.input-ip-address-control-1.0.min.js')
# assets.register('js_all', js)

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner

def auth_user(object, token):
    session['logged_in'] = True
    session['userid'] = object['current_identity']
    session['username'] = object['current_username']
    session['email'] = object['current_email']
    session['role'] = object['current_role']
    session['name'] = object['current_name']
    session['token'] = token

@app.route('/')
def index():
    return render_template('layout/base.html', data = session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('signin.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login = requests.post('http://localhost:5000/login', json={ "username": username, "password":password })
        try:
            jwtoken = login.json()['access_token']
            headers = {'Authorization': 'Bearer %s' % jwtoken}
            auth =  requests.get('http://localhost:5000', headers = headers).json()
            auth_user(auth, jwtoken)
            return index()
        except Exception as e:
            print e
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    logout = requests.delete('http://localhost:5000/logout', headers = headers).json()
    # return jsonify(logout)
    session.pop('logged_in', None)
    session.pop('userid', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('role', None)
    session.pop('token', None)
    return redirect(url_for('login'))


@app.route('/users', methods=['GET'])
@login_required
def users():
    print session['token']
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }    
    users = requests.get('http://localhost:5000/users', headers = headers).json()
    # print devices
    return render_template('userlist.html', users = users)

@app.route('/users/delete', methods=['POST'])
@login_required
def deleteuser():
    print session['token']
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    userid = request.form.getlist('users_id[]')[0]
    try:
        users = requests.delete('http://localhost:5000/users/delete', headers = headers, json={ "users_id": userid }).json()
        return redirect(url_for('users'))
    except Exception as e:
        return redirect(url_for('users'))

@app.route('/users/<string:username>', methods=['GET'])
@login_required
def userdetail(username):
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    userdetail = requests.get('http://localhost:5000/users/%s' % username, headers = headers).json()
    return render_template('userdetail.html', userdetail = userdetail)

@app.route('/register', methods=['POST','GET'])
@login_required
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        headers = { 'Authorization' : 'Bearer %s' % session['token'] }
        try:
            requests.post('http://localhost:5000/register', headers = headers, json={ "name": name, "username":username, "email" : email, "password" : password, "role" : role })
            return redirect(url_for('users'))
        except Exception as e:
            print e
            return redirect(url_for('register'))

@app.route('/devices/create', methods=['POST', 'GET'])
@login_required
def createdevice():
    if request.method == 'GET':
        return render_template('createdevice.html')
    elif request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        location = request.form['location']
        address = request.form['address']

        serviceNameList = request.form.getlist('servicename[]')
        serviceList = request.form.getlist('service[]')
        serviceArray = []
        for index, value in enumerate(request.form.getlist('servicename[]')):
            serviceArray.append({ 'servicename' : request.form.getlist('servicename[]')[index],
                    'command' : request.form.getlist('service[]')[index]})
        print serviceArray

        headers = { 'Authorization' : 'Bearer %s' % session['token'] }
        try:
            requests.post('http://localhost:5000/devices/create', headers = headers, json={ "name": name, "type":type, "location" : location, "address" : address, "service" : serviceArray })
            return redirect(url_for('devices'))
        except Exception as e:
            print e
            return redirect(url_for('createdevice'))

@app.route('/devices/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def editdevices(id):
    if request.method == 'GET':
        print session['token']
        headers = { 'Authorization' : 'Bearer %s' % session['token'] }
        devicedetail = requests.get('http://localhost:5000/devices/%s' % id, headers = headers).json()

        subscriber = []
        try:
            for subscribe in devicedetail['subscribed_by']:
                subscriber.append(subscribe['id'])
            return render_template('editdevice.html', devicedetail = devicedetail, subscriber = subscriber)
        except Exception as e:
            return render_template('editdevice.html', devicedetail = devicedetail)
    elif request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        location = request.form['location']
        address = request.form['address']

        headers = { 'Authorization' : 'Bearer %s' % session['token'] }
        try:
            editdevice = requests.post('http://localhost:5000/devices/edit/%s' % id, headers = headers, json={ "name": name, "type":type, "location" : location, "address" : address })
            return redirect(url_for('devices'))
        except Exception as e:
            return redirect(url_for('editdevices'))


@app.route('/devices/delete', methods=['POST'])
@login_required
def deletedevice():
    print session['token']
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    deviceid = request.form.getlist('deviceid[]')[0]
    try:
        devices = requests.delete('http://localhost:5000/devices/delete', headers = headers, json={ "deviceid": deviceid }).json()
        return redirect(url_for('devices'))
    except Exception as e:
        return redirect(url_for('devices'))


@app.route('/devices', methods=['GET'])
@login_required
def devices():
    print session['token']
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    devices = requests.get('http://localhost:5000/devices', headers = headers).json()
    # return devices
    return render_template('devicelist.html', devices = devices)


@app.route('/devices/<string:id>', methods=['GET'])
@login_required
def devicedetail(id):
    print session['token']
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    devicedetail = requests.get('http://localhost:5000/devices/%s' % id, headers = headers).json()
    # print devicedetail['subscribed_by']
    subscriber = []
    servicesubscriber = []
    try:
        for subscribe in devicedetail['subscribed_by']:
            subscriber.append(subscribe['id'])

        print subscriber
        print '\n'
        print servicesubscriber
        return render_template('devicedetail3.html', devicedetail = devicedetail, subscriber = subscriber)
        # return jsonify({'msg':'test'})
    except Exception as e:
        print e
        return render_template('devicedetail3.html', devicedetail = devicedetail)
        # return jsonify({'msg':'test'})

@app.route('/service/edit', methods=['POST'])
@login_required
def editoid():
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    dataDict = []
    serviceNow = []
    for index, value in enumerate(request.form.getlist('service[]')):
        serviceNow.append(request.form.getlist('serviceid[]')[index])
        if request.form.getlist('serviceid[]')[index] == '':
            dataDict.append({ 'id' : request.form.getlist('serviceid[]')[index],
                        'servicename' : request.form.getlist('servicename[]')[index],
                        'command' : request.form.getlist('service[]')[index],
                        'deviceid' : request.referrer.split('/')[4]})
        else:
            dataDict.append({ 'id' : request.form.getlist('serviceid[]')[index],
                        'servicename' : request.form.getlist('servicename[]')[index],
                        'command' : request.form.getlist('service[]')[index]})

    currentServiceid = []
    serviceData = requests.get('http://localhost:5000/devices/%s' % request.referrer.split('/')[4], headers = headers).json()
    for service in serviceData['service']:
        currentServiceid.append(service['id'])

    dataToDelete = set(currentServiceid) - set(serviceNow)
    for data in dataToDelete:
        print data
        try:
            deleteservice = requests.delete('http://localhost:5000/service/delete', headers = headers, json={ "service_id": data })
        except Exception as e:
            pass

    print dataDict
    for data in dataDict:
        if data['id'] == '':
            try:
                editservice = requests.post('http://localhost:5000/service/create', headers = headers, json=data)
            except Exception as e:
                return redirect(url_for('devices'))
        else:
            try:
                editservice = requests.post('http://localhost:5000/service/edit', headers = headers, json=data)
            except Exception as e:
                return redirect(url_for('devices'))

    return jsonify({ 'msg' : 'request success' })

@app.route('/subscribe/devices', methods=['POST'])
@login_required
def subscribedevice():
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    subscribe = requests.post('http://localhost:5000/subscribe/devices', headers = headers, json={ "deviceid": request.form['deviceid'] }).json()
    return redirect(request.url_root+'devices/%s' % request.form['deviceid'])

@app.route('/unsubscribe/devices', methods=['POST'])
@login_required
def unsubscribedevice():
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    unsubscribe = requests.post('http://localhost:5000/unsubscribe/devices', headers = headers, json={ "deviceid": request.form['deviceid'] }).json()
    for i in request.form.getlist('oid_id[]'):
        unsubscribeoid = requests.post('http://localhost:5000/unsubscribe/oid', headers = headers, json={ "oid_id": i }).json()
    return redirect(request.url_root+'devices/%s' % request.form['deviceid'])

@app.route('/subscribe/oid', methods=['POST'])
@login_required
def subscribeoid():
    oid = request.form['data']
    # print oid
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    subscribe = requests.post('http://localhost:5000/subscribe/service', headers = headers, json={ "service_id": oid }).json()
    return jsonify( { 'res' : 'success'} )

@app.route('/unsubscribe/oid', methods=['POST'])
@login_required
def unsubscribeoid():
    oid = request.form['data']
    # print oid
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    unsubscribe = requests.post('http://localhost:5000/unsubscribe/service', headers = headers, json={ "service_id": oid }).json()
    return jsonify( { 'res' : 'success'} )

@app.route('/monitor', methods=['GET'])
@login_required
def monitor():
    headers = { 'Authorization' : 'Bearer %s' % session['token'] }
    monitor = requests.get('http://localhost:5000/users/%s' % session['username'], headers = headers).json()
    return render_template('monitor.html', monitor = monitor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
