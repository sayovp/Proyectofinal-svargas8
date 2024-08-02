import unittest
from models.productos import Productos

class TestProductos(unittest.TestCase):
    
    def test_calcular_calorias(self):
       producto = Productos.query.get(1)
       self.assertEqual(producto.calcular_calorias(),100)

    def test_calcular_costo(self):
       producto = Productos.query.get(2) 
       self.assertEqual(producto.calcular_costo(),3500)     
       
    def test_calcular_rentabilidad(self):
       producto = Productos.query.get(2)
       self.assertEqual(producto.calcular_rentabilidad(), 1500)



