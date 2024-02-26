from flask import jsonify, request
from app.models import db, Usuario, Postagem, Curtida, PostagemUsuario
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_SERVER_ERROR = 500

def obter_postagens():
    id = request.args.get('id')
    nome_autor = request.args.get('nome_autor')

    if id:
        postagens = Postagem.query.filter_by(id=id).first()
    elif nome_autor:
        postagens = Postagem.query.filter_by(nome_autor=nome_autor).all()
    else:
        postagens = Postagem.query.all()

    postagens_json = [{
        'id': postagem.id,
        'titulo': postagem.titulo,
        'texto': postagem.texto,
        'nome_autor': postagem.nome_autor,
        'datahora_postagem': postagem.datahora_postagem.strftime("%Y-%m-%d %H:%M:%S")
    } for postagem in postagens]

    return jsonify({'postagens': postagens_json}), HTTP_OK

def criar_postagem():
    try:
        dados_postagem = request.get_json()

        nova_postagem = Postagem(
            titulo=dados_postagem['titulo'],
            texto=dados_postagem['texto'],
            nome_autor=dados_postagem['nome_autor'],
            datahora_postagem=datetime.utcnow()
        )

        db.session.add(nova_postagem)
        db.session.commit()

        nova_relacao = PostagemUsuario(
            usuario_id=dados_postagem['usuario_id'],
            postagem_id=nova_postagem.id
        )

        db.session.add(nova_relacao)
        db.session.commit()

        return jsonify({'mensagem': 'Postagem criada com sucesso!'}), HTTP_CREATED
    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR
    
def excluir_postagem(id_postagem):
    try:
        postagem = Postagem.query.get(id_postagem)

        if postagem:
            db.session.delete(postagem)
            db.session.commit()
            return jsonify({'mensagem': 'Postagem excluída com sucesso!'}), HTTP_OK
        else:
            return jsonify({'erro': 'Postagem não encontrada'}), HTTP_NOT_FOUND

    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR
    
def editar_postagem(id_postagem):
    try:
        dados_postagem = request.get_json()

        postagem = Postagem.query.get(id_postagem)

        if not postagem:
            return jsonify({'erro': 'Postagem não encontrada'}), HTTP_NOT_FOUND

        postagem.titulo = dados_postagem.get('titulo', postagem.titulo)
        postagem.texto = dados_postagem.get('texto', postagem.texto)
        postagem.nome_autor = dados_postagem.get(
            'nome_autor', postagem.nome_autor)

        db.session.commit()

        return jsonify({'mensagem': 'Postagem editada com sucesso!'}), HTTP_OK

    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR