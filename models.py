import configparser

from datetime import datetime
from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine

Base = declarative_base()

from sqlalchemy.orm import sessionmaker

def connect_prb_workflow_database():
    config = configparser.RawConfigParser()
    config.read('/eai/apps/framework/v3/utils/eai.properties')
    db = dict(config.items('prb_workfront'))
    return create_engine(f"mssql+pymssql://{db['user']}:{db['password']}@{db['host']}/{db['database']}")

#engine = create_engine("mssql+pymssql://workfront_admin:w0rKfr0nt@323@MSSQLD2016E607.mtvn.ad.viacom.com/PRB_RPT")
engine = connect_prb_workflow_database() 
Session = sessionmaker(bind=engine)
sessionMSSQL = Session()

def bulk_insert(items):
    global sessionMSSQL
    sessionMSSQL.bulk_save_objects(items)
    sessionMSSQL.commit()
    
def get_next_report_id():
    global sessionMSSQL
    return sessionMSSQL.query(func.max(ProjectReport.report_id)).scalar()

def get_next_program_id():
    global sessionMSSQL
    last_id = sessionMSSQL.query(func.max(Program.program_detail_id)).scalar()
    return last_id+1 if last_id else 1

def get_processed_files():
    global sessionMSSQL
    processed_files = sessionMSSQL.query(ProjectReport.processed_file_name).distinct()
    return processed_files
        
class Book(Base):
    __tablename__ = 'MTS_PRB_PROJECT_REPORT'
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(DateTime, nullable=False, default=datetime.utcnow())
    typ = Column(String(4000), nullable=False)
    file = Column(String(4000), nullable=True)

class UserBookSchedule(Base):
    __tablename__ = 'MTS_PRB_PROJECT_REPORT_DETAIL'
    id = Column(Integer, primary_key=True, autoincrement=False)
    days = Column(Integer)
    hours = Column(Integer)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    book = Column(Integer, ForeignKey('book.id'))
    user = Column(Integer, ForeignKey('user.id'))

class User(Base):
    __tablename__ = 'MTS_PRB_PROGRAM_DETAIL'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(250))
    nick = Column(String(250), nullable=False)
    portfolio_group = Column(String(4000), nullable=True)

# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
class UserBook(Base):
    id = Column(Integer, primary_key=True, autoincrement=False)
    book = 
    user = 
    days =
    current = 
    hours = 
