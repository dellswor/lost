# Read in some data
data = """user1,manager\nuser2,worker\nuser3,worker\nuser4,manager\nuser5,exec"""

# Read in map data
mapdata = list()
with open('map.txt') as f:
    state = 0
    for line in f:
        if state==0:
            if line.startswith('----'):
                state=1
                continue
        if state==1:
            if line.startswith('('):
                state=2
            else:
                mapdata.append(line.strip())
        if state==2:
            pass
mapdict = dict()
for e in mapdata:
    (role,pk) = e.split(',')
    mapdict[role.strip()]=pk.strip()


# Prepare the data for the roles table
rows = data.split('\n')
roles = dict()
for row in rows:
    (uname,role) = row.split(',')
    print("INSERT INTO users (username,role_fk) VALUES ('%s','%s');"%(uname,mapdict[role]))
