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
from RatesBot.Tools.LoggerLib import *
from RatesBot.Tools.Kwargs import Kwargs
from RatesBot.Tools.ScreenColors import clr
from bs4 import BeautifulSoup
import urllib.request
from RatesBot.DB.RatesDB import RatesDB
import RatesBot.Config as cfg

class ServiceBase(Logger, Kwargs):
    '''Common base class for all services that provide rates'''
    
    def __init__(self, *args, **kwargs):
        super(ServiceBase, self).__init__(*args, **kwargs)
        
        self.url = self.init_kwarg('url')
        self.service_name = self.init_kwarg('service_name')
        self.total_units = self.init_kwarg('total_units', default=1)
        self.page = ""
        self.soup = ""
        self._rate_morning = 0.00
        self._rate_evening = 0.00
        self._prices_text = ""
        self.db = RatesDB(conn_string=cfg.db['conn_string'])
        self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers = {'User-Agent':self.user_agent,} 

    @property
    def rate_morning(self):
        return self._rate_morning
        
    @rate_morning.setter
    def rate_morning(self,value):
        self._rate_morning = value
    
    @property
    def rate_evening(self):
        return self._rate_evening
        
    @rate_evening.setter
    def rate_evening(self,value):
        self._rate_evening = value
        
    @property
    def current_value_morning(self):
        
        return self.total_units*self._rate_morning
        
    @property
    def current_value_evening(self):
        return self.total_units*self._rate_evening
        
    @property
    def value_text_morning(self):
        return "\n\nTotal Value ({} units @ {}) : {}".format(self.total_units, self._rate_morning, self.current_value_morning)
    
    @property
    def value_text_evening(self):
        return "\n\nTotal Value ({} units @ {}) : {}".format(self.total_units, self._rate_evening, self.current_value_evening)
    
    @property
    def value_text(self):
        return self.value_text_morning + self.value_text_evening
    
    @property
    def prices_text(self):
        return self._prices_text + self.value_text
    
    def __read_url(self):
        
        self.logger.info("Reading website: {}".format(self.url))
        req = urllib.request.Request(self.url, headers=self.headers)
        response = urllib.request.urlopen(req)
        self.page = response.read()
        
    def __parse_html(self):
        
        self.logger.info("Parsing HTML: {}".format(self.url))
        
        self.soup = BeautifulSoup(self.page,features="html.parser")

    def db_save(self):
        '''Save rates to the database'''
        
        self.db.insert_rate(self)
        self.db.session.close()
        self.db.session.remove()
        self.logger.info("Rates saved to Database")
        
    def db_last_rates(self):
        '''Get the last rates inserted in the DB for the service'''

        last_rates = self.db.get_last_rates(self)
        self.db.session.close()
        self.db.session.remove()
        self.logger.debug("Last rates from DB: {}".format(str(last_rates)))
        
        return last_rates

    def get_rates(self):
        '''
        Retreive rates from a provider.
        This method should be implemented for each of the derived classes that will be implemented for each of the service.
        It should populate the fields - _prices_text, _rate_morning and _rate_evening after scraping the service and return prices_text
        '''
        self.__read_url()
        self.__parse_html()
            
    def rates_changed(self):
        '''Check latest rates from a service and compare to saved rates from last time the rates were checked.'''

        self.logger.debug("Current rates from {} : {}".format(self.service_name, "[{}, {}]".format(self.rate_morning,self.rate_evening)))

        if [self.rate_morning,self.rate_evening] == self.db_last_rates():
            return False
        else:
            self.db_save()
            
            return True

    def format_rate(self, rate):
        return 0.00 if (rate == "" or rate == "-") else float(rate.split()[0])

 
class KTRates(ServiceBase):
    '''Class derived from ServiceBase. Retrieves gold rates from www.khaleejtimes.com'''

    def __init__(self, *args, **kwargs):
        
        url = "http://www.khaleejtimes.com/gold-forex/"
        service_name = "Khaleej Times"
        super(KTRates, self).__init__(url=url, service_name=service_name, *args, **kwargs)
        
    def get_rates(self):
    
        super(KTRates, self).get_rates()
        
        for i in self.soup.findAll('tr',{'class':'gold_r1'}):

            if "22" in i.td.text:
                rates = i.text.replace(" ","").replace("\r\n","").strip().split("\n")
                break
        
        self._prices_text += "\n{} gold prices updated\n".format(self.service_name)
        
        if len(rates) == 5:
           self._prices_text += "\nMorning - {}\nEvening - {}\nYesterday - {}".format(rates[1], rates[2], rates[4])
    
        if len(rates) == 4:
            self._prices_text += "\nMorning - {}\nEvening - {}\nYesterday - {}".format(rates[1], rates[2], rates[3])
        
        self._rate_morning = self.format_rate(rates[1])
        self._rate_evening = self.format_rate(rates[2])
        
        return self.prices_text

class GPDRates(ServiceBase):
    '''Class derived from ServiceBase. Retrieves gold rates from www.goldpricesdubai.com'''
    
    def __init__(self, *args, **kwargs):
    
        url = "http://www.goldpricesdubai.com/"
        service_name = "Gold Prices Dubai"
        super(GPDRates, self).__init__(url=url, service_name=service_name, *args, **kwargs)
        
        
    def get_rates(self):
    
        super(GPDRates, self).get_rates()
        
        rates = [txt.text for txt in self.soup.findAll('table',{'class':'now'})[0].findChildren('tr')[4].findChildren('td')]
        self._prices_text += "\n{} gold prices updated\n".format(self.service_name)
        self._prices_text += "\nRate - {}".format(rates[0])
        self._rate_morning = self.format_rate(rates[0])
        self._rate_evening = 0.00
        
        return self.prices_text
        
        