import unittest
from models.heladeria import Heladeria

class TestHeladeria(unittest.TestCase):
    
    def test_vender(self):
        resultado = self.heladeria.vender(2)
        self.assertEqual(resultado, 'venta exitosa')

    def test_vender_no(self):
        resultado = self.heladeria.vender(3)
        self.assertEqual(resultado, 'no existencia de chips chocolate')

    def test_mejor_producto(self):
        result = Heladeria.mejor_producto()
        self.assertEqual(result, 'El producto Malteada de fresa tiene la mejor rentabilidad con 4800')


