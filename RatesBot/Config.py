#!/usr/bin/python
# 
# Simple telegram bot to track the rates of tradeables available on the web (e.g. Gold),
# and send notifications on Telegram if the rate of a tradeable changes.
# Copyright (C) 2018
# Salman Raza <raza.salman@gmail.com>
#
# GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>
import json
import os

def get_engine_string():

    retval = None

    if db['dialect'] is not None:
    
        retval = db['dialect']+"://"+db['uname']+":"+db['password']+"@"+db['host']
        
        if db['port'] is not None:
            retval = retval+":"+db['port']
            
        retval = retval + "/"+db['dbname']
        
        if db['options'] is not None:
            
            retval=retval+"?"
            
            for opt,val in db['options'].items():
                retval = retval + opt + "=" + val + "&"
    else:

        retval = "sqlite:///rates.db"

    return retval


def load_config():
    
    with open(os.path.expanduser('~/.config/ratesbot/config.json')) as data:
        config = json.load(data)

    globals().update(config)
    db['conn_string'] = get_engine_string()

load_config()
