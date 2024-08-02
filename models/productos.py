from db import db
from models.ingredientes import Ingredientes


producto_ingrediente = db.Table('producto_ingrediente',
            db.Column('idproducto',db.Integer, db.ForeignKey("productos.idproductos"), primary_key = True), 
             db.Column('idingrediente',db.Integer, db.ForeignKey("ingredientes.idingredientes"),primary_key = True))


class Productos(db.Model):
    idproductos = db.Column(db.Integer, primary_key = True)
    nombreProducto = db.Column(db.String(45), nullable = False)
    precioProducto = db.Column(db.Integer, nullable = False)
    tipoProducto  = db.Column(db.Boolean, nullable = False)
    volumen = db.Column(db.Integer, nullable = True)
    tipoVaso = db.Column(db.String(45), nullable = True)

    ingredientes = db.relationship('Ingredientes',secondary=producto_ingrediente, lazy='subquery', backref=db.backref('productos', lazy=True))


    def calcular_calorias(self):
        for ingrediente in self.ingredientes:
            cantidad =+ ingrediente.numeroCalorias
        
        return cantidad
    
    def calcular_costo(self):
        for ingrediente in self.ingredientes:
            costo =+ ingrediente.precioIngrediente
        return costo
    
    def calcular_rentabilidad(self):
        costo = 0
        for ingrediente in self.ingredientes:
            costo =+ ingrediente.precioIngrediente
        return self.precioProducto - costo
    
    def dict_productos(self):
        producto_dict = {
            "idProducto": self.idproductos,
            "nombreProducto": self.nombreProducto,
            "precioProducto": self.precioProducto
        }
        return producto_dict
