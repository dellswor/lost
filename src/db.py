from config import dbname, dbhost, dbport
import psycopg2

def html_select_roles():
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
        cur = conn.cursor()
        sql = "SELECT role FROM roles"
        cur.execute(sql)
        conn.commit()
        res = cur.fetchall()
        role_options = list()
        for r in res:
            role_options.append('<OPTION VALUE="%s">%s</OPTION>'%(r[0],r[0]))
        return ''.join(role_options)

def html_select_fcodes():
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
        cur = conn.cursor()
        sql = "SELECT fcode,common_name FROM facilities ORDER by common_name"
        cur.execute(sql)
        conn.commit()
        res = cur.fetchall()
        fcode_options = list()
        for r in res:
            fcode_options.append('<OPTION VALUE="%s">%s</OPTION>'%(r[0],r[1]))
        return ''.join(fcode_options)

def fetch_facilities():
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
        cur = conn.cursor()
        sql = "SELECT fcode,common_name,username,f.create_dt FROM facilities f JOIN users u ON u.user_pk=f.create_user ORDER BY fcode"
        cur.execute(sql)
        conn.commit()
        res = cur.fetchall()
        facilities = list()
        for r in res:
            d = dict()
            d['fcode'] = r[0]
            d['cname'] = r[1]
            d['uname'] = r[2]
            d['cdate'] = r[3]
            facilities.append(d)
        return facilities

def fetch_assets():
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
        cur = conn.cursor()
        sql = "SELECT asset_tag,description,a.create_dt,username FROM assets a JOIN users u ON u.user_pk=a.create_user ORDER BY asset_tag"
        cur.execute(sql)
        conn.commit()
        res = cur.fetchall()
        facilities = list()
        for r in res:
            d = dict()
            d['atag'] = r[0]
            d['desc'] = r[1]
            d['date'] = r[2]
            d['name'] = r[3]
            facilities.append(d)
        return facilities

def put_facility(fcode,cname,uname):
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
        cur = conn.cursor()
        sql = "SELECT count(*) FROM users WHERE username=%s"
        cur.execute(sql,(uname,))
        res = cur.fetchone()[0]
        if res != 1:
            # fail due to bad username
            return "Illegal user adding facility"
        sql = "SELECT count(*) FROM facilities WHERE fcode=%s or common_name=%s"
        cur.execute(sql,(fcode,cname))
        res = cur.fetchone()[0]
        if res != 0:
            # fail due to duplicate
            return "Duplicate asset. Addition rejected"
        sql = "INSERT INTO facilities (common_name,fcode,create_dt,create_user) SELECT %s,%s,now(),user_pk FROM users WHERE username=%s"
        cur.execute(sql,(cname,fcode,uname))
        conn.commit()
    return None

def put_asset(atag,desc,fcode,uname):
    with psycopg2.connect(dbname=dbname,host=dbhost,port=dbport) as conn:
        cur = conn.cursor()
        sql = "SELECT count(*) FROM users WHERE username=%s"
        cur.execute(sql,(uname,))
        res = cur.fetchone()[0]
        if res != 1:
            # fail due to bad username
            return "Illegal user adding asset"
        sql = "SELECT count(*) FROM assets WHERE asset_tag=%s"
        cur.execute(sql,(atag,))
        res = cur.fetchone()[0]
        if res != 0:
            # fail due to duplicate
            return "Duplicate asset. Addition rejected"
        sql = "INSERT INTO assets (asset_tag,description,create_dt,create_user) SELECT %s,%s,now(),user_pk FROM users WHERE username=%s RETURNING asset_pk"
        cur.execute(sql,(atag,desc,uname))
        a_pk = cur.fetchone()[0]
        sql = "INSERT INTO asset_at (asset_fk,facility_fk,arrive_dt) SELECT %s,facility_pk,now() FROM facilities WHERE fcode=%s"
        cur.execute(sql,(a_pk,fcode))
        conn.commit()
    return None