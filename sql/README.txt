This directory holds some tools for configuring the LOST database and migrating legacy OSNAP data.

Files:
README.txt - This readme file
create_tables.sql - A script to generate the base tables
import_data.sh - A script to import some data into the base tables
gen_inserts1.py - Python script to generate some data to import
gen_inserts2.py - Python script to generate some data to import
do_inserts.py - Python script to generate and import data


-------------------------------------
--  Example import_data.sh script
-------------------------------------
The demo import_data.sh script demonstrates how to import data using python to generate sql scripts. Here is output setting up and running the import_data.sh script.

[osnapdev@osnap-image sql]$ createdb lost
[osnapdev@osnap-image sql]$ psql lost -f create_tables.sql 
CREATE TABLE
CREATE TABLE
[osnapdev@osnap-image sql]$ bash import_data.sh lost 5432
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
[osnapdev@osnap-image sql]$ psql lost
psql (9.5.5)
Type "help" for help.

lost=# select * from users;
 user_pk | username | role_fk 
---------+----------+---------
       1 | user1    |       3
       2 | user2    |       2
       3 | user3    |       2
       4 | user4    |       3
       5 | user5    |       1
(5 rows)

lost=# select * from roles;
 role_pk | rolename 
---------+----------
       1 | exec
       2 | worker
       3 | manager
(3 rows)

lost=# 


-----------------------------
-- python interacting with the database directly example
-----------------------------
[osnapdev@osnap-image sql]$ createdb lost
[osnapdev@osnap-image sql]$ psql lost -f create_tables.sql 
CREATE TABLE
CREATE TABLE
[osnapdev@osnap-image sql]$ python3 do_inserts.py lost 5432
[osnapdev@osnap-image sql]$ psql lost
psql (9.5.5)
Type "help" for help.

lost=# select * from users;
 user_pk | username | role_fk 
---------+----------+---------
       1 | user1    |       3
       2 | user2    |       2
       3 | user3    |       2
       4 | user4    |       3
       5 | user5    |       1
(5 rows)

lost=#


-------------------------------------
-- First cut at queries for testing with real OSNAP data imported
-------------------------------------
To test the LOST database after the OSNAP data has been migrated, the following queries have been suggests. These queries are untested but should have the right basic structure. If you compare the queries to the entity relationship diagram you should be able to trace the path between the assets and facilities.

/* This query successfully returning all assets at least once is enough to get credit */
SELECT fcode,asset_tag 
FROM assets a
JOIN asset_at aa  ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.asset_fk=f.facility_pk

/* This query is more complex... only the facility an asset is currently at. Assets in transit will be missed */
SELECT fcode,asset_tag 
FROM assets a
JOIN asset_at aa  ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.asset_fk=f.facility_pk
WHERE aa.arrive_dt < now() and (aa.depart_dt is NULL or aa.depart_dt > now())

/* This query should pick up the assets currently in transit */
SELECT fcode,asset_tag 
FROM assets a
JOIN asset_on aa  ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.asset_fk=f.facility_pk
WHERE aa.load_dt < now() and (aa.unload_dt is NULL or aa.unload_dt > now())
