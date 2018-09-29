from RatesBot.Tools.LoggerLib import *
from RatesBot.Tools.ScreenColors import clr
from bs4 import BeautifulSoup
import urllib2

from RatesBot.DB.RatesDB import RatesDB

import RatesBot.Config as cfg

Service_logger = colorlog.getLogger('RatesBot.Service')
#Service_logger.setLevel(logging.DEBUG)

            
class ServiceBase(object):
    '''Common base class for all services that provide rates'''
    
    def __init__(self, *args, **kwargs):
    
        
        self.url = kwargs['url']
        
        self.service_name = kwargs['service_name']
        
        self.total_units = kwargs['total_units'] if (kwargs.get('total_units') is not None) else 1
        
        self.page = ""
        
        self.soup = ""
        
        self._rate_morning = 0.00
        
        self._rate_evening = 0.00
        
        self._prices_text = ""
        
        self.db = RatesDB(db_uname=cfg.db['uname'],db_pass=cfg.db['pass'],db_host=cfg.db['host'],db_name=cfg.db['name'])

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
        
        Service_logger.info("Reading website: {}".format(self.url))
        self.page = urllib2.urlopen(self.url)
        
    def __parse_html(self):
        
        Service_logger.info("Parsing HTML: {}".format(self.url))
        
        self.soup = BeautifulSoup(self.page.read(),features="html.parser")

        
    
    def db_save(self):
        '''Save rates to the database'''
        
        self.db.insert_rate(self)
        
        self.db.session.close()
        
        self.db.session.remove()
        
        Service_logger.info("Rates saved to Database")
        
        
    def db_last_rates(self):
        '''Get the last rates inserted in the DB for the service'''
        
        Service_logger.debug("Getting last saved rates from the DB")

        last_rates = self.db.get_last_rates(self)
        
        self.db.session.close()
        
        self.db.session.remove()
        
        Service_logger.debug("Last rates from DB: {}".format(str(last_rates)))
        
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
        
        rates = self.soup.findAll('table',{'class':'now'})[0].findChildren('tr')[6].text.strip().split("\n")
        
        self._prices_text += "\n{} gold prices updated\n".format(self.service_name)
        
        self._prices_text += "\nMorning - {}\nEvening - {}".format(rates[1],rates[2])
        
        self._rate_morning = self.format_rate(rates[1])
        
        self._rate_evening = self.format_rate(rates[2])
        
        return self.prices_text
        
        