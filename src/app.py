from flask import Flask, render_template, request, session, redirect
from config import dbname, dbhost, dbport
import psycopg2
import datetime

from db import html_select_roles, html_select_fcodes, fetch_facilities, put_facility, fetch_assets, put_asset, user_role, del_asset, fetch_userinfo, valid_fcode, valid_atag, put_transit_req, fetch_need_approval, fetch_transit_req, mark_approved, mark_rejected, put_load_unload, fetch_need_load

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def check_login():
    # Is there a username in the session
    if not 'username' in session:
        return False
    # Get the user information
    (uname, urole, uactv) = fetch_userinfo(session['username'])
    if uactv is None:
        return False
    session['username']=uname
    session['role']=urole
    return True
    
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

@app.route('/asset_report',methods=('GET','POST'))
def asset_report():
    form_fields=dict()
    data = list()
    if request.method=='GET':
        # Set form defaults
        form_fields['fcode']=''
        form_fields['rdate']=datetime.datetime.utcnow().isoformat()
    if request.method=='POST':
        # Read last values
        if 'fcode' in request.form and 'date' in request.form:
            form_fields['fcode']=request.form['fcode']
            form_fields['rdate']=request.form['date']
        else:
            form_fields['fcode']=None
            form_fields['rdate']=datetime.datetime.utcnow().isoformat()
        # Run query
        with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
            cur = conn.cursor()
            sql = '''SELECT asset_tag,description,common_name,arrive_dt,depart_dt,disposed_dt,fcode
            FROM asset_at aa
            JOIN facilities f ON aa.facility_fk=f.facility_pk
            JOIN assets a ON a.asset_pk=aa.asset_fk
            WHERE (arrive_dt is null or arrive_dt<=%s) and
                  (depart_dt is null or depart_dt>=%s) and
                  (disposed_dt is null or disposed_dt>=%s)'''
            if form_fields['fcode']=='':
                sql += " order by asset_tag asc"
                cur.execute(sql,(form_fields['rdate'],form_fields['rdate'],form_fields['rdate']))
            else:
                sql += " and f.fcode=%s order by asset_tag asc"
                cur.execute(sql,(form_fields['rdate'],form_fields['rdate'],form_fields['rdate'],form_fields['fcode']))
            res = cur.fetchall()
            conn.commit()
            for r in res:
                e = dict()
                e['atag']=r[0]
                e['desc']=r[1]
                e['cname']=r[2]
                if r[3] is None:
                    e['adate']=''
                else:
                    e['adate']=r[3]
                if r[4] is None and r[5] is None:
                    e['ddate']=''
                elif r[4]:
                    e['ddate']=r[4]
                else:
                    e['ddate']=r[5]
                e['fcode']=r[6]
                data.append(e)
    fv = html_select_fcodes(selected=form_fields['fcode'])
    return render_template('asset_report.html',fvals=form_fields,fcode_options=fv,data=data)
        
@app.route('/transfer_report',methods=('GET','POST'))
def transfer_report():
    pass

@app.route('/request_transfer',methods=('GET','POST'))
def req_transfer():
    pass
    
@app.route('/dashboard',methods=('GET',))
def dashboard():
    if not check_login():
        return redirect('login')
    to_approve = None
    to_load    = None
    if session['role']=='Facilities Officer':
        to_approve = fetch_need_approval()
    if session['role']=='Logistics Officer':
        to_load = fetch_need_load()
    return render_template('dashboard.html',username=session['username'],to_approve=to_approve,to_load=to_load)

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

@app.route('/transfer_req', methods=('GET','POST'))
def transfer_req():
    if not check_login():
        return redirect('login')
    if not session['role']=='Logistics Officer':
        session['error']='Only a Logistics Officer may initiate a transfer request'
        return redirect('error')
    if request.method=='GET':
        fv = html_select_fcodes()
        return render_template('init_transfer.html',fcode_options=fv)
    if request.method=='POST':
        # Parse the input
        if 'src_fcode' in request.form and 'dst_fcode' in request.form and 'a_tag' in request.form:
            src_fcode=request.form['src_fcode']
            dst_fcode=request.form['dst_fcode']
            a_tag    =request.form['a_tag']
        else:
            session['error']="Bad form inputs"
            return redirect('error')
            
        # Validate input
        if not valid_fcode(src_fcode):
            session['error']="Bad source"
            return redirect('error')
        if not valid_fcode(dst_fcode):
            session['error']="Bad destination"
            return redirect('error')
        if not valid_atag(a_tag):
            session['error']="Bad asset tag"
            return redirect('error')
            
        # Add the transit request
        is_ok = put_transit_req(session['username'],a_tag,src_fcode,dst_fcode)
        if is_ok:
            session['error']="Transit request created successfully"
        else:
            session['error']="An error occurred trying to make the request"
        return redirect('error')

@app.route('/approve_req', methods=('GET','POST'))
def approve_req():
    if not check_login():
        return redirect('login')
    if not session['role']=='Facilities Officer':
        session['error']='Only a Facilities Officer may approve/reject a transfer request'
        return redirect('error')
    if request.method=='GET':
        print(request.args)
        if not 'id' in request.args:
            print("no id")
            session['error']='Invalid Request'
            return redirect('error')
        else:
            transit_pk=int(request.args['id'])
            try:
                data = fetch_transit_req(transit_pk)
            except:
                print("db error")
                session['error']='Invalid Request'
                return redirect('error')
            if not data['is_approved']==None:
                session['error']='Approvel already complete'
                return redirect('error')
            return render_template('approve_req.html',data=data)
    if request.method=='POST':
        if not 'id' in request.form or not 'submit' in request.form:
            session['error']='Invalid Request'
            return redirect('error')
        if request.form['submit']=='cancel':
            pass
        if request.form['submit']=='approve':
            mark_approved(session['username'],int(request.form['id']))
        if request.form['submit']=='reject':
            mark_rejected(session['username'],int(request.form['id']))
        return redirect('dashboard')

@app.route('/update_transit', methods=('GET','POST'))
def update_transit():
    if not check_login():
        return redirect('login')
    if not session['role']=='Logistics Officer':
        session['error']='Only a Logistics Officer may load/unload assets'
        return redirect('error')
    if request.method=='GET':
        print(request.args)
        if not 'id' in request.args:
            print("no id")
            session['error']='Invalid Request'
            return redirect('error')
        else:
            transit_pk=int(request.args['id'])
            try:
                data = fetch_transit_req(transit_pk)
            except:
                print("db error")
                session['error']='Invalid Request'
                return redirect('error')
            if data['load']==None:
                data['load']='YYYY-MM-DD'
            if data['unload']==None:
                data['unload']='YYYY-MM-DD'
            else:
                # Unloaded assets can't be updated here
                session['error']='asset already unloaded'
                return redirect('error')
            return render_template('update_req.html',data=data)
    if request.method=='POST':
        if not 'id' in request.form or not 'load' in request.form or not 'unload' in request.form or not 'submit' in request.form:
            session['error']='Invalid Request'
            return redirect('error')
        data=dict()
        data['id']=request.form['id']
        data['load']=request.form['load']
        data['unload']=request.form['unload']
        if data['unload']=='YYYY-MM-DD':
            data['unload']=None
        if request.form['submit']=='cancel':
            pass
        if request.form['submit']=='save':
            put_load_unload(session['username'],int(data['id']),data['load'],data['unload'])
        return redirect('dashboard')

if __name__=='__main__':
    app.debug = True
    app.run(port=8080, host='0.0.0.0')
