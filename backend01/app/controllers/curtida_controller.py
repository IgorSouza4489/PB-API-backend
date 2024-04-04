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

@jwt_required()
def adicionar_curtida(id_postagem):
    try:
        postagem = Postagem.query.get(id_postagem)
        if not postagem:
            return jsonify({'erro': 'Postagem não encontrada'}), HTTP_NOT_FOUND

        dados = request.get_json()
        usuario_id = dados.get('usuario_id')

        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), HTTP_NOT_FOUND

        if usuario in postagem.usuarios_curtiram:
            return jsonify({'mensagem': 'Usuário já curtiu esta postagem'}), HTTP_OK

        curtida = Curtida(usuario_id=usuario_id, postagem_id=id_postagem)
        db.session.add(curtida)
        db.session.commit()

        return jsonify({'mensagem': 'Curtida adicionada com sucesso'}), HTTP_CREATED

    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR

@jwt_required()
def obter_curtidas(id_postagem):
    try:
        postagem = Postagem.query.get(id_postagem)
        if not postagem:
            return jsonify({'erro': 'Postagem não encontrada'}), HTTP_NOT_FOUND

        curtidas = [curtida.usuario_id for curtida in postagem.curtidas]
        return jsonify({'curtidas': curtidas}), HTTP_OK

    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR
    
@jwt_required
def obter_postagens_mais_curtidas():
    try:
        postagens_mais_curtidas = db.session.query(Postagem, db.func.count(Curtida.id).label('num_curtidas')) \
            .join(Curtida).group_by(Postagem.id).order_by(db.desc('num_curtidas')).limit(4).all()

        postagens_curtidas_info = []
        for postagem, num_curtidas in postagens_mais_curtidas:
            postagens_curtidas_info.append({
                'titulo': postagem.titulo,
                'num_curtidas': num_curtidas,
                'nome_autor': postagem.nome_autor,
                'url_img': postagem.url_img
            })

        return jsonify({'postagens_mais_curtidas': postagens_curtidas_info}), HTTP_OK

    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR

@jwt_required
def obter_postagens_curtidas_mim(usuario_id):
    try:
        postagens_curtidas_mim = db.session.query(Postagem, db.func.count(Curtida.id).label('num_curtidas')) \
            .join(Curtida).filter(Postagem.usuario_id == usuario_id) \
            .group_by(Postagem.id).order_by(db.desc('num_curtidas')).limit(4).all()

        postagens_curtidas_info = []
        for postagem, num_curtidas in postagens_curtidas_mim:
            postagens_curtidas_info.append({
                'titulo': postagem.titulo,
                'num_curtidas': num_curtidas,
                'nome_autor': postagem.nome_autor,
            })

        return jsonify({'postagens_curtidas_mim': postagens_curtidas_info}), HTTP_OK

    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR
