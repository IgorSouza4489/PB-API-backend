from routes import obter_usuarios
from main import app

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_SERVER_ERROR = 500

def test_obter_usuarios():
    resposta = obter_usuarios()
    assert resposta.status_code == HTTP_OK