from flask import jsonify, request
from app.models import db, Usuario, Postagem, Curtida
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_SERVER_ERROR = 500

def obter_usuario_id():
    requested_user_id = request.args.get('id')

    if not requested_user_id:
        return jsonify({'message': 'Por favor, forneça o ID do usuário'}), 400

    usuario = Usuario.query.filter_by(id=requested_user_id).first()

    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    usuario_json = {
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'data_nascimento': usuario.data_nascimento,
    }

    return jsonify({'usuario': usuario_json}), 200

#@jwt_required()
def obter_usuarios():
    nome = request.args.get('nome')
    email = request.args.get('email')

    if nome:
        usuarios = Usuario.query.filter_by(nome=nome).all()
    elif email:
        usuarios = Usuario.query.filter_by(email=email).all()
    else:
        usuarios = Usuario.query.all()

    usuarios_json = [{
        'id': user.id, 'nome': user.nome,
        'email': user.email,
        'data_nascimento': user.data_nascimento,
        'senha': user.senha
    } for user in usuarios]
    
    return jsonify({'usuarios': usuarios_json}), HTTP_OK

#Deprecated
#@jwt_required()
def incluir_usuario():
    try:
        dados_usuario = request.get_json()
        data_nascimento = datetime.strptime(
            dados_usuario['data_nascimento'], '%d/%m/%Y').date()
        senha_hash = generate_password_hash(dados_usuario['senha'])

        novo_usuario = Usuario(
            nome=dados_usuario['nome'],
            email=dados_usuario['email'],
            data_nascimento=data_nascimento,
            senha=senha_hash)

        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({'mensagem': 'Usuário incluído com sucesso!'}), HTTP_CREATED
    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR
    

#Deprecated
#@jwt_required()
def fazer_login():
    dados_login = request.get_json()

    if 'email' not in dados_login or 'senha' not in dados_login:
        return jsonify({'erro': 'E-mail e senha são obrigatórios.'}), HTTP_BAD_REQUEST

    email = dados_login['email']
    senha = dados_login['senha']

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.senha, senha):
        return jsonify({'mensagem': 'Sucesso'}), HTTP_OK
    else:
        return jsonify({'erro': 'E-mail ou senha incorretos.'}), HTTP_UNAUTHORIZED