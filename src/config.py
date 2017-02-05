import json

import os
import pathlib

# This file contains logic for parsing the LOST configuration file.

cpath = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')

with cpath.open() as conf:
    c = json.load(conf)
    dbname = c['database']['dbname']
    dbhost = c['database']['dbhost']
    dbport = c['database']['dbport']

    lost_priv = c['crypto']['lost_priv']
    lost_pub  = c['crypto']['lost_pub']
    user_pub  = c['crypto']['user_pub']
    prod_pub  = c['crypto']['prod_pub']
