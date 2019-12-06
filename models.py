import configparser

from datetime import datetime
from sqlalchemy import Column, Integer, String, func
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

        
class Book(Base):
    __tablename__ = 'MTS_PRB_PROJECT_REPORT'
    report_id = Column(Integer, primary_key=True, autoincrement=False)
    load_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    processed_file_name = Column(String(4000), nullable=False)
    project_name = Column(String(4000), nullable=False)
    project_manager = Column(String(4000), nullable=True)
    report_date = Column(String(4000), nullable=True)
    project_status = Column(String(4000), nullable=True)

class UserBookSchedule(Base):
    __tablename__ = 'user_book_schedule'
    report_id = Column(Integer, primary_key=True, autoincrement=False)
    report_section_id = Column(Integer)
    user = Column(Integer)
    book = Column(Integer)
    report_section_col_1 = Column(String(4000), nullable=True)
    report_section_col_2 = Column(String(4000), nullable=True)
    report_section_col_3 = Column(String(4000), nullable=True)
    report_section_col_4 = Column(String(4000), nullable=True)

class UserBook(Base):
    __tablename__ = 'MTS_PRB_PROGRAM_DETAIL'
    program_detail_id = Column(Integer, primary_key=True, autoincrement=False)
    user = Column(Integer)
    book = Column(Integer)
    current_status = Column(Integer)
    processed_file_name = Column(String(250), nullable=False)
    project_name = Column(String(4000), nullable=True)
    program_number = Column(String(4000), nullable=True)
    program_name = Column(String(4000), nullable=True)
    product_owner = Column(String(4000), nullable=True)
    tech_lead = Column(String(4000), nullable=True)
    business_sponsor = Column(String(4000), nullable=True)
    portfolio_group = Column(String(4000), nullable=True)
