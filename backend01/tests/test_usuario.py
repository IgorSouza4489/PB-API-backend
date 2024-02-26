from run import app

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_SERVER_ERROR = 500

client = app.test_client()

def test_obter_usuarios():
    resposta = client.get('/usuarios')
    assert resposta.status_code == HTTP_OK