from flask import Flask, render_template, request, session, redirect
from config import dbname, dbhost, dbport
import psycopg2

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/error',methods=('GET',))
def error():
    if 'error' in session.keys():
        msg = session['error']
        del session['error']
        return render_template('error_msg.html',msg=msg)
    return render_template('error_msg.html',msg='Unknown error')

@app.route('/create_user', methods=('GET','POST'))
def create_user():
    if request.method=='GET':
        return render_template('create_user.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            uname = request.form['username']
            upass = request.form['password']
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
                cur = conn.cursor()
                # Clean up the aged out records
                sql = "delete from users where create_dt < now() - interval '15 minutes';"
                cur.execute(sql)
                # Check if the user exists
                sql = "select count(*) from users where username=%s"
                cur.execute(sql,(uname,))
                res = cur.fetchone()[0]
                if res != 0:
                    # Username taken
                    session['error'] = 'Username %s is taken.'%uname
                    return redirect('error')
                # Add the user
                sql = "insert into users (username,password,create_dt) VALUES (%s,%s,now())"
                cur.execute(sql,(uname,upass))
                session['error'] = 'Username %s added.'%uname
                return redirect('error')
        session['error'] = 'Invalid form fields'
        return redirect('error')
    session['error'] = 'Invalid HTTP method %s'%request.method
    return redirect('error')

if __name__=='__main__':
    app.debug = True
    app.run(port=8080, host='0.0.0.0')
