from flask import Flask, render_template, request, session, redirect
from config import dbname, dbhost, dbport
import psycopg2

from db import html_select_roles, html_select_fcodes, fetch_facilities, put_facility, fetch_assets, put_asset, user_role, del_asset

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def user_is(role):
    if not 'username' in session:
        return False
    if role == user_role(session['username']):
        return True
    return False
    
@app.route('/')
@app.route('/login',methods=('GET','POST'))
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            uname = request.form['username']
            upass = request.form['password']
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
                cur = conn.cursor()
                # Checking login
                sql = "select count(*) from users where username=%s and password=%s"
                cur.execute(sql,(uname,upass))
                conn.commit()
                res = cur.fetchone()[0]
                if res != 1:
                    # Username taken
                    session['error'] = 'Authentication failed for %s.'%uname
                    return redirect('error')
                session['username']=uname
                return redirect('dashboard')
        session['error'] = 'Invalid form fields'
        return redirect('error')
    session['error'] = 'Invalid HTTP method %s'%request.method
    return redirect('error')

@app.route('/add_facility',methods=('GET','POST'))
def add_facility():
    if request.method=='GET':
        flist = fetch_facilities()
        return render_template('add_facility.html',flist=flist)
    if request.method=='POST':
        # Want the user name for my accounting (not part of reqs)
        if not 'username' in session:
            uname = 'system'
        else:
            uname = session['username']
        # Read the form data
        fcode = request.form['fcode']
        cname = request.form['cname']
        res = put_facility(fcode,cname,uname)
        if res is not None:
            if res == 'Illegal user adding facility':
                del session['username']
            session['error']=res
            return redirect('error')
        return redirect('add_facility')

@app.route('/add_asset',methods=('GET','POST'))
def add_asset():
    if request.method=='GET':
        alist = fetch_assets()
        fv = html_select_fcodes()
        return render_template('add_asset.html',alist=alist,fcode_options=fv)
    if request.method=='POST':
        # Want the user name for my accounting (not part of reqs)
        if not 'username' in session:
            uname = 'system'
        else:
            uname = session['username']
        # Read the form data
        atag = request.form['atag']
        desc = request.form['desc']
        fcode = request.form['fcode']
        res = put_asset(atag,desc,fcode,uname)
        if res is not None:
            if res == 'Illegal user adding asset':
                del session['username']
            session['error']=res
            return redirect('error')
        return redirect('add_asset')

@app.route('/dispose_asset',methods=('GET','POST'))
def dispose_asset():
    # Access control
    if not user_is('Logistics Officer'):
        session['error']='Only Logistics Officer may dispose assets'
        return redirect('error')
    if request.method=='GET':
        return render_template('dispose_asset.html')
    if request.method=='POST':
        atag = request.form['atag']
        date = request.form['date']
        res = del_asset(atag,date)
        if res is not None:
            session['error']=res
            return redirect('error')
        return redirect('dashboard')
        
@app.route('/dashboard',methods=('GET',))
def dashboard():
    return render_template('dashboard.html',username=session['username'])

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
        sv = html_select_roles()
        return render_template('create_user.html',role_options=sv)
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            uname = request.form['username']
            upass = request.form['password']
            urole = request.form['role']
            with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
                cur = conn.cursor()
                # Check if the user exist
                sql = "select count(*) from users where username=%s"
                cur.execute(sql,(uname,))
                res = cur.fetchone()[0]
                if res != 0:
                    # Username taken
                    session['error'] = 'Username %s is taken.'%uname
                    return redirect('error')
                # Add the user
                sql = "insert into users (username,password,create_dt,role) VALUES (%s,%s,now(),%s)"
                cur.execute(sql,(uname,upass,urole))
                conn.commit()
                session['error'] = 'Username %s added.'%uname
                return redirect('error')
        session['error'] = 'Invalid form fields'
        return redirect('error')
    session['error'] = 'Invalid HTTP method %s'%request.method
    return redirect('error')

if __name__=='__main__':
    app.debug = True
    app.run(port=8080, host='0.0.0.0')
