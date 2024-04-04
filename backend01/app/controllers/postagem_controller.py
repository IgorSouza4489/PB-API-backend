from flask import jsonify, request
from app.models import db, Usuario, Postagem, Curtida, Comentario
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
import replicate
from http import HTTPStatus
import os

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_SERVER_ERROR = 500

@jwt_required()

def obter_postagens():
    id = request.args.get('id')
    nome_autor = request.args.get('nome_autor')

    if id:
        postagens = Postagem.query.filter(Postagem.usuario_id == id).all()
    elif nome_autor:
        postagens = Postagem.query.filter_by(nome_autor=nome_autor).all()
    else:
        postagens = Postagem.query.all()

    postagens_json = []
    for postagem in postagens:
        comentarios = Comentario.query.filter(Comentario.postagem_id == postagem.id).all()
        comentarios_json = []
        for comentario in comentarios:
            comentarios_json.append({
                'id': comentario.id,
                'texto': comentario.texto,
                'nome_autor': comentario.nome_autor,
                
            })

        num_curtidas = Curtida.query.filter(Curtida.postagem_id == postagem.id).count()
        postagens_json.append({
            'id': postagem.id,
            'titulo': postagem.titulo,
            'texto': postagem.texto,
            'nome_autor': postagem.nome_autor,
            'usuario_id': postagem.usuario_id,
            'datahora_postagem': postagem.datahora_postagem.strftime("%Y-%m-%d %H:%M:%S"),
            'num_curtidas': num_curtidas,
            'comentarios': comentarios_json,
            'url_img': postagem.url_img
        })

    return jsonify({'postagens': postagens_json}), 200

@jwt_required()
def criar_postagem():
    try:
        dados_postagem = request.get_json()

        nova_postagem = Postagem(
            titulo=dados_postagem['titulo'],
            url_img = gerar_img(dados_postagem['texto']),
            texto=dados_postagem['texto'],
            nome_autor=dados_postagem['nome_autor'],
            usuario_id=dados_postagem['usuario_id'],
            datahora_postagem=datetime.utcnow()
        )

        db.session.add(nova_postagem)
        db.session.commit()

        return jsonify({'mensagem': 'Postagem criada com sucesso!'}), HTTP_CREATED
    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR
    
@jwt_required()
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
    
@jwt_required()
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


def gerar_img(txt_receita):
    os.environ["REPLICATE_API_TOKEN"] = "r8_MqSHdujQTcaKb6c2d525FVnTWoGCpBB3mcXO5"
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                    "prompt": f"Top-down close-up shot: A table with a white plate placed in the center, filled with:" + txt_receita,
                    "width": 1024,
                    "height": 1024,
                    "refine": "no_refiner",
                    "scheduler": "K_EULER",
                    "lora_scale": 0.6,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "apply_watermark": False,
                    "high_noise_frac": 0.8,
                    "negative_prompt": "",
                    "prompt_strength": 0.8
                    }
            )
        img_url = output[0]
        print(img_url)
    except Exception as e:
        img_url = "https://www.designi.com.br/images/preview/10802356.jpg"
        print(e)

    return img_url


def adicionar_comentario(id_postagem):
    try:
        dados_comentario = request.get_json()

        texto = dados_comentario.get('texto')
        nome_autor = dados_comentario.get('nome_autor', 'Anônimo')
        

        novo_comentario = Comentario(
            texto=texto,
            nome_autor=nome_autor,
            datahora_postagem=datetime.utcnow(),
            postagem_id=id_postagem,
        )

        db.session.add(novo_comentario)
        db.session.commit()

        return jsonify({'mensagem': 'Comentário adicionado com sucesso!'}), HTTP_CREATED
    except Exception as e:
        return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR
    
def get_comentarios_por_postagem(id_postagem):
    try:
        comentarios = Comentario.query.filter_by(postagem_id=id_postagem).all()
        comentarios_formatados = [
            {
                'id': comentario.id,
                'texto': comentario.texto,
                'nome_autor': comentario.nome_autor,
                'datahora_postagem': comentario.datahora_postagem.isoformat()
            }
            for comentario in comentarios
        ]

        return jsonify(comentarios_formatados), HTTPStatus.OK
    except Exception as e:
        return jsonify({'erro': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR