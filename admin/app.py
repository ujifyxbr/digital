import os

import flask_admin
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_security.utils import encrypt_password
from flask_admin import helpers as admin_helpers
from flask import Flask, url_for, redirect

from models import User, Role, Student, Event
from flask_admin import BaseView
from views import SecuredView, UserView, StudentView, EventView
from extensions import db


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

admin = flask_admin.Admin(
    app,
    'Monitoring',
    base_template='index.html',
    template_mode='bootstrap3',
)

#admin.add_view(SecuredView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
#admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(SecuredView(Student, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Student"))
admin.add_view(SecuredView(Event, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Event"))

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

@app.route('/')
def index():
    return redirect('/admin/login/')

if __name__ == '__main__':

    app.run(debug=True, port=5050)