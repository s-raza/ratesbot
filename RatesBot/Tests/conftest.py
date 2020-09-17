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

import pytest
from RatesBot.Tools.LoggerLib import *
from RatesBot.Tools.ScreenColors import clr
from RatesBot.DB.RatesDB import RatesDB
from RatesBot.Services.Service import *


@pytest.fixture(scope="session")
def db(request):
        
    db = RatesDB(db_name="ratesdb_test")
    
    #Function for teardown operations
    def fin():
        
        print(clr.red("\n===Tearing down===\n"))
        db.session.close()
        db.session.remove()
        db.base.metadata.drop_all(db.engine)
        
        print(clr.red("\n===Executed drop_all on the DB===\n"))
        
    request.addfinalizer(fin)
    
    return db

    
    