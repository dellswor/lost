# Read in some data
data = """user1,manager\nuser2,worker\nuser3,worker\nuser4,manager\nuser5,exec"""

# Prepare the data for the roles table
rows = data.split('\n')
roles = dict()
for row in rows:
    (uname,role) = row.split(',')
    roles[role]=1
for role in roles.keys():
    print("INSERT INTO roles (rolename) VALUES ('%s');"%role)
print("SELECT rolename || ',' || role_pk FROM roles;")
