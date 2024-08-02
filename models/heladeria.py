from models.ingredientes import Ingredientes
from models.productos import Productos


class Heladeria():
    def __init__(self) -> None:
        self.ingredientes = Ingredientes.query.all()
        self.productos = Productos.query.all()

    def vender(self,idproducto):
        producto = Productos.query.get(idproducto)
        try:
            for ingredientes in producto.ingredientes:
                valid = True
                if ingredientes.tipoIngrediente and ingredientes.inventario <0.2:
                    valid = False
                    raise ValueError(f"no existencia de {ingredientes.nombreIngrediente}")
                elif ingredientes.inventario < 2:
                    valid = False
                    raise ValueError(f"no existencia de {ingredientes.nombreIngrediente}")

            if valid:
                for ingredientes in producto.ingredientes:
                    cantidad = ingredientes.inventario - (0.2 if ingredientes.tipoIngrediente else 2)
                    ingrediente = Ingredientes.query.get(ingredientes.idingredientes)
                    ingrediente.act_ingrediente(cantidad)
            return 'venta exitosa'   
        except ValueError as e:
            return e
        
    def mejor_producto(self):
        valor1=0
        maxRentabilidad = 0
        nomProducto=''
        for producto in self.productos:
            valor1 = producto.calcular_rentabilidad()
            if valor1 > maxRentabilidad:
                maxRentabilidad= valor1
                nomProducto = producto.nombreProducto
        return f"El producto {nomProducto} tiene la mejor rentabilidad con {maxRentabilidad}"