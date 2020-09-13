from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(schema='monitoring')
db = SQLAlchemy(metadata=metadata)