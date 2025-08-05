from routes.home import home_route
from database.database import db
from database.models.pizzas import Pedidos

def configure_all(app):
    configure_routes(app)
    configure_db()

def configure_routes(app):
    app.register_blueprint(home_route)

def configure_db():
    db.connect()
    db.create_tables([Pedidos])