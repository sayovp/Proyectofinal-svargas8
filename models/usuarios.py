from flask_login import UserMixin
from db import db

class Usuarios(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(45), nullable = False)
    password = db.Column(db.Integer, nullable = False)
    es_admin  = db.Column(db.Boolean, nullable = False)
    es_empleado  = db.Column(db.Boolean, nullable = False)

    def __init__(self, id, username, password, es_admin, es_empleado):
        self.id = id
        self.username = username
        self.password = password
        self.es_admin = es_admin
        self.es_empleado = es_empleado 
