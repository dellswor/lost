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
