from flask import jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import db, UserApi

def registrar_usuario_api():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    new_user = UserApi(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

def fazer_login_api():
    data = request.get_json()
    user = UserApi.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Credenciais inválidas'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200