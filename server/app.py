#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
import os
import json


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    app.logger.info("Index route called")
    return "<h1>Code challenge</h1>"

class RestaurantsResource(Resource):
    def get(self):
        try:
            restaurants = Restaurant.query.all()
            data = [restaurant.to_dict(include=['id', 'name', 'address']) for restaurant in restaurants]
            response = make_response(json.dumps(data), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            app.logger.error(f"Error retrieving restaurants: {e}")
            response = make_response(json.dumps({"error": "Internal Server Error"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

class RestaurantResource(Resource):
    def get(self, id):
        try:
            restaurant = Restaurant.query.get(id)
            if restaurant:
                data = restaurant.to_dict(include=['id', 'name', 'address', 'restaurant_pizzas'])
                response = make_response(json.dumps(data), 200)
            else:
                response = make_response(json.dumps({"error": "Restaurant not found"}), 404)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            app.logger.error(f"Error retrieving restaurant: {e}")
            response = make_response(json.dumps({"error": "Internal Server Error"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

    def delete(self, id):
        try:
            restaurant = Restaurant.query.get(id)
            if restaurant:
                db.session.delete(restaurant)
                db.session.commit()
                response = make_response("", 204)
            else:
                response = make_response(json.dumps({"error": "Restaurant not found"}), 404)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting restaurant: {e}")
            response = make_response(json.dumps({"error": "Internal Server Error"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

class PizzasResource(Resource):
    def get(self):
        try:
            pizzas = Pizza.query.all()
            data = [pizza.to_dict(include=['id', 'ingredients', 'name']) for pizza in pizzas]
            response = make_response(json.dumps(data), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            app.logger.error(f"Error retrieving pizzas: {e}")
            response = make_response(json.dumps({"error": "Internal Server Error"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

class RestaurantPizzasResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            pizza_id = data.get('pizza_id')
            restaurant_id = data.get('restaurant_id')
            price = data.get('price')

            if not pizza_id or not restaurant_id or price is None or not (1 <= price <= 30):
                response = make_response(json.dumps({"errors": ["validation errors"]}), 400)
                response.headers['Content-Type'] = 'application/json'
                return response

            restaurant = Restaurant.query.get(restaurant_id)
            pizza = Pizza.query.get(pizza_id)

            if not restaurant or not pizza:
                response = make_response(json.dumps({"error": "Restaurant or Pizza not found"}), 404)
                response.headers['Content-Type'] = 'application/json'
                return response

            new_restaurant_pizza = RestaurantPizza(
                restaurant_id=restaurant_id,
                pizza_id=pizza_id,
                price=price
            )

            db.session.add(new_restaurant_pizza)
            db.session.commit()
            data = {
                    'id': new_restaurant_pizza.id,
                    'restaurant': new_restaurant_pizza.restaurant,
                    'pizza': new_restaurant_pizza.pizza,
                    'price': new_restaurant_pizza.price
                    }
            response = make_response(json.dumps(data), 201)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating restaurant pizza: {e}")
            response = make_response(json.dumps({"error": "Internal Server Error"}), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

api.add_resource(RestaurantsResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzasResource, '/pizzas')
api.add_resource(RestaurantPizzasResource, '/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)

