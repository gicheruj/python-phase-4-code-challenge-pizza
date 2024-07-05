from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    pizzas = relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurants = relationship("RestaurantPizza", back_populates="pizza", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey("restaurants.id"))
    pizza_id = db.Column(db.Integer, ForeignKey("pizzas.id"))
    price = db.Column(db.Integer, nullable=False)

    restaurant = relationship("Restaurant", back_populates="pizzas")
    pizza = relationship("Pizza", back_populates="restaurants")

    @validates("price")
    def validate_price(self, key, price):
        if not isinstance(price, int) or price < 1 or price > 30:
            raise ValueError("Price must be an integer between 1 and 30.")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
    