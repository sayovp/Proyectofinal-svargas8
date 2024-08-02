from flask import render_template, make_response
from flask_restful import Resource
from models.ingredientes import Ingredientes
from db import db

class IngredientesController(Resource):
    def get(self):
        ingredientes = Ingredientes.query.all()
        return make_response(render_template("ingredientes.html", ingredientes = ingredientes))