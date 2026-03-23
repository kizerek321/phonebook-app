# SQLAlchemy database models
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts",
    metadata = MetaData()

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)