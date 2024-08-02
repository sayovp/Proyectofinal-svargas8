import unittest
from models.ingredientes import Ingredientes

class TestIngredientes(unittest.TestCase):
    def test_ingredientesano(self):
        ingrediente= Ingredientes.query.get(1)
        self.assertEqual(ingrediente.ingredientesano(),True)

    def test_abastecer(self):
        ingrediente = Ingredientes.query.get(2)
        inicial = ingrediente.inventario
        ingrediente.abastecer()
        self.assertEqual(ingrediente.abastecer(), inicial + 5)

    def test_renovar_inventario(self):
        ingrediente = Ingredientes.query.get(3)
        self.assertEqual(ingrediente.inventario, 0)

    