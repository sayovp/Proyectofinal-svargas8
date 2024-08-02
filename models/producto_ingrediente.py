from db import db

class Producto_ingrediente(db.Model):
    idproducto = db.Column(db.Integer, db.ForeignKey("productos.idproductos"), primary_key = True)
    idingrediente = db.Column(db.Integer, db.ForeignKey("ingredientes.idingredientes"),primary_key = True)