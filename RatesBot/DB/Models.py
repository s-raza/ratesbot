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
