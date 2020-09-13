from flask_security import UserMixin, RoleMixin
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import synonym

from extensions import db

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(255), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(255), nullable=False, server_default=u'')
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    ip = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    events = db.relationship('Event', backref='student', lazy=True)

    def __init__(self, **kwargs):
        super(Student, self).__init__(**kwargs)

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    img_filename = synonym('img_path')
    img_path = db.Column(db.String(), unique=True)
    img_datetime = db.Column(db.DateTime(timezone=True), default=db.func.now())
    img_metadata = db.Column(JSONB)
    alert_id = db.Column(db.Integer, db.ForeignKey('alert.id'))
    is_alert = db.Column(db.Boolean())
    alert_type = db.String(db.String()) # due to some problems with admin's preview
    img = db.Column(db.Binary())

    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)

class Alert(db.Model):
    __tablename__ ='alert'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_alert = db.Column(db.String(255))
    events = db.relationship('Event', backref='alert', lazy=True)

    def __init__(self, **kwargs):
        super(Alert, self).__init__(**kwargs)
