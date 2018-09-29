from RatesBot.DB.RatesDB import RatesDB
from RatesBot.DB.Models import *
from RatesBot.Services.Service import *

from RatesBot.Tools.ScreenColors import clr

def test_connection_to_db(db):

    
    assert db.session is not None
    
    
def test_add_service(db):


    service_name = "service1"
    url = "https://service1"
    
    db.inserted = db._RatesDB__add_service(service_name,url)
    
    db.session.commit()
    
    added = db.session.query(Service).filter_by(name=service_name,url=url).first()
    
    
    assert added.name == service_name
    assert added.url == url
 

def function_tester(db,function, rate_morning=130.00, rate_evening=135.00):

    for service in ServiceBase.__subclasses__():
        
        srv = service()
        
        print clr.red("\n===TESTING [{}] - {}===\n".format(srv.service_name, function.__name__))
        
        srv.rate_morning = rate_morning
        srv.rate_evening = rate_evening
        
        function(db,srv)
    

def get_service_inst(db,s):
    
    
    s_inst = db._RatesDB__get_service_inst(s)

    s_inst_from_db = db.session.query(Service).filter_by(name=s_inst.name,url=s_inst.url).first()
    
    assert s_inst.name == s_inst_from_db.name
    assert s_inst.url == s_inst_from_db.url
    
 
def test_get_service_inst_all(db):

    function_tester(db,get_service_inst)
   

def insert_rate(db,srv):
    
    db.inserted = db.insert_rate(srv)
    
    added = db.session.query(Rate).filter(Rate.id == db.inserted.rates[len(db.inserted.rates)-1].id).one()
    
    assert added.rate_morning == srv.rate_morning
    assert added.rate_evening == srv.rate_evening
    
    
def test_insert_rate_all(db):

    function_tester(db,insert_rate)

    
def get_last_rates(db,srv):
    
    db.inserted = db.insert_rate(srv)
    
    last_rates = db.get_last_rates(srv)
    
    assert last_rates == [srv.rate_morning,srv.rate_evening]

def test_get_last_rates_all(db):
    
    function_tester(db,get_last_rates)
    
    
    
    