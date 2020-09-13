from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
#Session = sessionmaker(bind=engine)
metadata = MetaData(schema='monitoring')
Base = declarative_base(metadata=metadata)

db_session = scoped_session(sessionmaker(bind=engine))