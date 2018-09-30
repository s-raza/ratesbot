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

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

class Service(Base):
    
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), unique=True)
    url = Column(String(512))
    
    
    
class Rate(Base):
    
    __tablename__ = "rates"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    rate_date = Column(DateTime, default=func.now())
    
    rate_morning = Column(Float)
    
    rate_evening = Column(Float)
    
    service_id = Column(Integer, ForeignKey('services.id'))
    
    service = relationship("Service", back_populates="rates")
    
Service.rates = relationship("Rate", back_populates="service")
