from flask import Flask
from flask_cors import CORS
from app.models import db
from app.routes import configure_routes

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['*'])
    app.config.from_pyfile('app/config.py')
    db.init_app(app)
    #http://localhost:8081/
    configure_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)