from RatesBot.DB.Models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from RatesBot.Tools.LoggerLib import *
from RatesBot.Tools.ScreenColors import clr
import RatesBot.Config as cfg

ratesdb_logger = colorlog.getLogger('Service_bot.ratesdb')

class RatesDB():
    
    def __init__(self, *args, **kwargs):
        
        
        self.db_uname = kwargs['db_uname'] if (kwargs.get('db_uname') is not None) else "ratesuser"
        self.db_pass = kwargs['db_pass'] if (kwargs.get('db_pass') is not None) else "ratesuserpass"
        self.db_host = kwargs['db_host'] if (kwargs.get('db_host') is not None) else "localhost"
        self.db_name = kwargs['db_name'] if (kwargs.get('db_name') is not None) else "ratesdb"
        
        self.conn_str = "mysql+mysqldb://{}:{}@{}/{}?charset=utf8mb4".format(self.db_uname, self.db_pass, self.db_host, self.db_name)
        
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
        
        return inst
        
        
        
    def get_last_rates(self, service):
        '''Query the database to get the last row inserted into the database'''
        
        service_inst = self.__get_service_inst(service)
        
        #last_insert = self.session.query(Rate).filter_by(id=select([func.max(Rate.id)])).one()
        
        last_insert = self.session.query(Rate).filter(Rate.id == self.session.query(func.max(Rate.id)).filter(Rate.service_id==service_inst.id)).one()
        
        return [last_insert.rate_morning,last_insert.rate_evening]
        
        
        
    def insert_rate(self, service):
        '''Insert rates into the database, which were queried from the service'''
        
        service_inst = self.__get_service_inst(service)
        
        service_inst.rates.append(Rate(rate_morning=service.rate_morning, rate_evening=service.rate_evening))
        
        self.session.commit()
        
        return service_inst

        
        
        
        
        