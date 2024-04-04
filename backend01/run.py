from flask import Flask
from flask_cors import CORS
from app.models import db
from app.routes import configure_routes
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:8080'])
    app.config.from_pyfile('app/config.py')
    db.init_app(app)
    configure_routes(app)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)

    # Adicionar Access-Control-Allow-Origin à resposta
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'

        return response

    return app

app = create_app()
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
