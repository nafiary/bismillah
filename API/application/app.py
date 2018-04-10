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
from pprint import pprint
import requests

DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/devices')
def index():
    devices = requests.get('http://localhost:5000/devices').json()
    print devices
    return render_template('devicelist.html', devices = devices)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
