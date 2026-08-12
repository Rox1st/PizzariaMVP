from flask import Flask
from .repositories.database import init_db
from .controllers.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'pizzaria.db'
    init_db(app.config['DATABASE'])
    register_routes(app)
    return app
