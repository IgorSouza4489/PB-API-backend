from flask import jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import db, UserApi, Usuario
from datetime import datetime

def registrar_usuario_api():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    data_nascimento = datetime.strptime(data.get('data_nascimento'), '%Y-%m-%d').date()
    senha = data.get('senha')
    if not nome or not email or not data_nascimento or not senha:
        return jsonify({'message': 'Por favor, forneça todos os campos necessários'}), 400
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'message': 'Este endereço de e-mail já está em uso'}), 400
    hashed_password = generate_password_hash(senha).decode('utf-8')
    novo_usuario = Usuario(nome=nome, email=email, data_nascimento=data_nascimento, senha=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso!'}), 201


def registrar_usuario_api1():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    new_user = UserApi(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

def fazer_login_api():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if not usuario or not check_password_hash(usuario.senha, data['senha']):
        return jsonify({'message': 'Credenciais inválidas'}), 401
    access_token = create_access_token(identity=usuario.id)
    return jsonify(access_token=access_token), 200

def fazer_login_api1():
    data = request.get_json()
    user = UserApi.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Credenciais inválidas'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200