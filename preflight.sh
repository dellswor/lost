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
cd ..

# Install the wsgi files
cp -R src/* $HOME/wsgi

