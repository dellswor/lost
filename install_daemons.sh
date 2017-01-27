#! /usr/bin/bash

# This script is for downloading and installing some daemons that might be
# needed later in the project... The output of this script is worth 0 points
# when grading the term project due to the incorrect application versions.

# Usage:
#    ./install_daemons.sh <prefix>

if [ "$#" -ne 1 ]; then
    echo "Usage: ./install_daemons.sh <prefix>"
    exit;
fi

# The following steps build the wrong version of each of the programs
git clone https://github.com/postgres/postgres.git pg_build
cd pg_build
git checkout REL9_6_STABLE
./configure --prefix=$1
make install
cd ..

curl https://archive.apache.org/dist/httpd/httpd-2.4.12.tar.gz > httpd-2.4.12.tar.gz
tar -zxf httpd-2.4.12.tar.gz
cd httpd-2.4.12
./configure --prefix=$1
make install
cd ..

rm -rf pg_build httpd-2.4.12.tar.gz httpd-2.4.12
