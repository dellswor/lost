from flask import Flask, render_template, request
from config import dbname, dbhost, dbport

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

import json
@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    # request.form is only populated for POST messages
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/goodbye')
def goodbye():
    if request.method=='GET' and 'mytext' in request.args:
        return render_template('goodbye.html',data=request.args.get('mytext'))

    # request.form is only populated for POST messages
    if request.method=='POST' and 'mytext' in request.form:
        return render_template('goodbye.html',data=request.form['mytext'])
    return render_template('index.html')

