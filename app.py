from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from db import db
from controllers.ingredientes_controller import IngredientesController
import pymysql

import os


pymysql.install_as_MySQLdb()

load_dotenv(overwrite=True)

secret_key =  os.urandom(24)


app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("URL_BD")}/{os.getenv("TABLE_BD")}'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://sql10723330:CD9JplNqjh@sql10.freemysqlhosting.net/sql10723330'
app.config["SECRET_KEY"] = secret_key
db.init_app(app)
api = Api(app)
#db = SQLAlchemy(app)

#from controllers.heladeria_controller import *
import controllers.heladeria_controller
#@app.route('/')
#def main():
#    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)


#api.add_resource(IngredientesController, '/ingredientes')
#api.add_resource(, '/ingredientes')'''


    