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

from RatesBot.DB.Models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from RatesBot.Tools.LoggerLib import *
from RatesBot.Tools.Kwargs import Kwargs
from RatesBot.Tools.ScreenColors import clr
import RatesBot.Config as cfg

class RatesDB(Logger, Kwargs):
    
    def __init__(self, *args, **kwargs):
        super(RatesDB, self).__init__(*args, **kwargs)
        
        self.conn_str = self.init_kwarg('conn_string')
        self.engine = create_engine(self.conn_str)
        self.base = Base
        self.base.metadata.create_all(self.engine)
        self.session = scoped_session( sessionmaker(bind=self.engine) )
        
    def __get_service_inst(self, service):
        
        '''Get the instance of a service from the database, create it if it does not exist by name.'''
        
        service_inst = self.session.query(Service).filter_by(name=service.service_name).first()
        
        if service_inst is None:
            new_service = self.__add_service(service_name=service.service_name, url=service.url)
            return new_service
        else:
            return service_inst
        
    def __add_service(self, service_name, url):
        '''Insert a new service in the databse'''
        
        inst = Service(name=service_name, url=url)
        self.session.add(inst)
        self.session.commit()
        
        return inst
        
    def get_last_rates(self, service):
        '''Query the database to get the last row inserted into the database'''
        
        service_inst = self.__get_service_inst(service)
        last_insert = self.session.query(Rate).filter(Rate.id == self.session.query(func.max(Rate.id)).filter(Rate.service_id==service_inst.id)).first()
        
        if last_insert is not None:
            return [last_insert.rate_morning,last_insert.rate_evening]
        else:
            return [0.00,0.00]
        
    def insert_rate(self, service):
        '''Insert rates into the database, which were queried from the service'''
        
        service_inst = self.__get_service_inst(service)
        service_inst.rates.append(Rate(rate_morning=service.rate_morning, rate_evening=service.rate_evening))
        self.session.commit()

        return service_inst
