import psycopg2
import sys

# Read in some data
data = """user1,manager\nuser2,worker\nuser3,worker\nuser4,manager\nuser5,exec"""

# Setup the database connection
conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

# Prepare the data for the roles table
rows = data.split('\n')
roles = dict()
for row in rows:
    (uname,role) = row.split(',')
    roles[role]=1
for role in roles.keys():
    cur.execute("INSERT INTO roles (rolename) VALUES (%s)",(role,))
    cur.execute("SELECT role_pk FROM roles WHERE rolename=%s",(role,))
    roles[role] = cur.fetchone()[0]
for row in rows:
    (uname,role) = row.split(',')
    cur.execute("INSERT INTO users (username,role_fk) VALUES (%s,%s)",(uname,roles[role],))

# commit the changes to the database
conn.commit()

# close the connection nicely
cur.close()
conn.close()
