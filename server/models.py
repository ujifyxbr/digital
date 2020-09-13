from flask_security import UserMixin, RoleMixin
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Unicode, func, Binary
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import synonym, relationship, backref

import db

# Define models
roles_users = Table(
    'roles_users',
    db.Base.metadata,
    Column('user_id', Integer(), ForeignKey('user.id')),
    Column('role_id', Integer(), ForeignKey('role.id'))
)

class Role(db.Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(db.Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary=roles_users,
                            backref=backref('user', lazy='dynamic'))

class Student(db.Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(255), nullable=False, server_default=u'')
    last_name = Column(Unicode(255), nullable=False, server_default=u'')
    email = Column(Unicode(255), nullable=False, server_default=u'', unique=True)
    #ip = Column(Unicode(255), nullable=False, server_default=u'', unique=True)
    active = Column(Boolean(), nullable=False, server_default='0')
    events = relationship('Event', backref='student', lazy=True)

    def __init__(self, **kwargs):
        super(Student, self).__init__(**kwargs)

class Event(db.Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    img_filename = synonym('img_path')
    img_path = Column(String(), unique=True)
    img_datetime = Column(DateTime(timezone=True), default=func.now())
    img_metadata = Column(JSONB)
    alert_id = Column(Integer, ForeignKey('alert.id'))
    is_alert = Column(Boolean())
    alert_type = Column(String())
    img = Column(Binary())

    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)

class Alert(db.Base):
    __tablename__ ='alert'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_alert = Column(String(255))
    events = relationship('Event', backref='alert', lazy=True)

    def __init__(self, **kwargs):
        super(Alert, self).__init__(**kwargs)
