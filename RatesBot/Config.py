
# # Telegram Bot information for sending messages
# bot_token = "626698985:AAGs85gUXr0nvfNfvx6tXqUVe2h-5U7GgFE"

# #ID of the user or group where the notifications will be sent
# chat_id = -282153463


# # MySQL database connection information
# db = {'uname': 'ratesuser',
#        'pass': 'ratesuserpass',
#        'host': 'localhost',
#        'name': 'ratesdb'}

# total_units = 500
#!/usr/bin/python

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
            
            for opt,val in db['options'].iteritems():
                retval = retval + opt + "=" + val + "&"
    else:

        retval = "sqlite:///rates.db"

    return retval


def load_config():
    
    with open(os.path.abspath('../config.json')) as data:
        config = json.load(data)

    globals().update(config)
    db['conn_string'] = get_engine_string()

load_config()

