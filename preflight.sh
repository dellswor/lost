#! /usr/bin/bash

# This script handles the setup that must occur prior to running LOST
# Specifically this script:
#    1. creates the database
#    2. imports the legacy data
#    3. copies the required source to $HOME/wsgi

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dbname>"
    exit;
fi

# Database prep
cd sql
psql $1 -f create_tables.sql
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xzf osnap_legacy.tar.gz
bash ./import_data.sh $1 5432
rm -rf osnap_legacy osnap_legacy.tar.gz
cd ..

# Install the wsgi files
cp -R src/* $HOME/wsgi
# Need to install the crypo library as well
cp util/osnap_crypto.py $HOME/wsgi

