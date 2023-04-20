from flask import Flask
from flask_mysqldb import MySQL

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qwerty1234'
app.config['MYSQL_DB'] = 'Shopsphere'

mysql = MySQL(app)

# pylint: disable=C0413:wrong-import-position
from main import routes
