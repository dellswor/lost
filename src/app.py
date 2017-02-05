from flask import Flask, render_template, request
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
from osnap_crypto import encrypt, decrypt_and_verify

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
    # Check if the call uses crypto
    if request.method=='POST' and 'signature' in request.form and \
            request.form['signature'] != '' and 'arguments' in request.form:
        # do the crypto, expect that hr is on the other side
        (data, skey, nonce) = decrypt_and_verify(request.form['arguments'], request.form['signature'], lost_priv, user_pub)
        
        # Process the request
        req=json.loads(data)
        
        # Prepare the response data
        dat = dict()
        dat['timestamp'] = req['timestamp']
        dat['result'] = 'OK'
        data = json.dumps(dat)
        
        # Encrypt and send the response
        data = encrypt(data,skey,nonce)
        return data
    
    # Try to handle as plaintext
    elif request.method=='POST' and 'arguments' in request.form:
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

