
from django.db import models
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
metadata = MetaData()


class DataSQLA(Base):
    __tablename__ = 'DataSQLA'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    lastprice = Column(Float)
    timeframe = Column(Integer)
    dataevent = Column(DateTime)

Base.metadata.create_all(bind=engine)



from django.db import models

# Create your models here.
