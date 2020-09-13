FROM python:slim

RUN pip install --upgrade pip
RUN pip install flask flask_security flask_admin flask_sqlalchemy flask_sqlalchemy
RUN pip install psycopg2-binary

COPY . /admin

EXPOSE 5050
CMD python admin/app.py