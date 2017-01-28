#! /bin/bash

# This script is for migrating OSNAP legacy data into the LOST database. The script 
# introduces a few specific defects during migration that will result in 0 points if 
# the defects appear during the term project grading.

# to speed up dev, put the db in a fresh state
dropdb $1
createdb $1
psql $1 -f create_tables.sql

# Load the security data
python3 prep_sec.py
psql $1 -f sec_load.sql
rm sec_load.sql

# Load the facilities -- A list is not provided in the data but may be inferred from the 
# provided data... This list should be asked for from the customer
psql $1 -f facilities_map.sql

# Handle the product data, such as it is
python3 prep_prod.py
psql $1 -f prod_load.sql
rm prod_load.sql