
from flask_admin.contrib import sqla
from flask_admin import BaseView, expose, form
from flask_security import current_user
from flask import Flask, url_for, redirect, render_template, request, abort, Markup

class SecuredView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True

class UserView(SecuredView):
    column_editable_list = ['email']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class StudentView(SecuredView):
    column_list = ['first_name', 'last_name', 'email', 'active']

class EventView(SecuredView):

    def _blob_formatter(view, context, model, name):
        if model.img is not None:
            return str(model.img[:10]) + '...'

    column_formatters = {
        'img': _blob_formatter
    }



