from flask import Flask
from models import db
from routes import configure_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:8080'])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    configure_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)