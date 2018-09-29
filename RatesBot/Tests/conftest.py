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
        
        print clr.red("\n===Tearing down===\n")
        db.session.close()
        db.session.remove()
        db.base.metadata.drop_all(db.engine)
        
        print clr.red("\n===Executed drop_all on the DB===\n")
        
    request.addfinalizer(fin)
    
    return db

    
    