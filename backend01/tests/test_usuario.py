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

def test_icluir_usuarios():
    dados_usuario = {
        'nome': 'Teste Teste1',
        'email': 'teste1@example.com',
        'data_nascimento': '01/01/1990',
        'senha': 'teste123'
    }

    resposta = client.post('/usuarios', json=dados_usuario)
    assert resposta.status_code == HTTP_CREATED

    resposta_json = resposta.get_json()
    assert resposta_json['mensagem'] == 'Usuário incluído com sucesso!'