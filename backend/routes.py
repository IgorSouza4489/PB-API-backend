from flask import jsonify, request
from models import db, Usuario, Postagem
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_SERVER_ERROR = 500


def rota_obter_usuarios(app):
    @app.route("/usuarios", methods=['GET'])
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
            'data_nascimento': user.data_nascimento
        }
            for user in usuarios]
        return jsonify({'usuarios': usuarios_json}), HTTP_CREATED


def rota_incluir_usuario(app):
    @app.route('/usuarios', methods=['POST'])
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


def rota_fazer_login(app):
    @app.route("/login", methods=["POST"])
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


def rota_obter_postagens(app):
    @app.route('/postagens', methods=['GET'])
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


def rota_criar_postagem(app):
    @app.route('/postagens', methods=['POST'])
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

            return jsonify({'mensagem': 'Postagem criada com sucesso!'}), HTTP_CREATED
        except Exception as e:
            return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR


def rota_excluir_postagem(app):
    @app.route('/postagens/<int:id_postagem>', methods=['DELETE'])
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


def rota_editar_postagem(app):
    @app.route('/postagens/<int:id_postagem>', methods=['PUT'])
    def editar_postagem(id_postagem):
        try:
            dados_postagem = request.get_json()

            postagem = Postagem.query.get(id_postagem)

            if not postagem:
                return jsonify({'erro': 'Postagem não encontrada'}), HTTP_NOT_FOUND

            postagem.titulo = dados_postagem.get('titulo', postagem.titulo)
            postagem.texto = dados_postagem.get('texto', postagem.texto)
            postagem.nome_autor = dados_postagem.get('nome_autor', postagem.nome_autor)

            db.session.commit()

            return jsonify({'mensagem': 'Postagem editada com sucesso!'}), HTTP_OK

        except Exception as e:
            return jsonify({'erro': str(e)}), HTTP_SERVER_ERROR


def configure_routes(app):
    rota_obter_usuarios(app)
    rota_incluir_usuario(app)
    rota_fazer_login(app)
    rota_obter_postagens(app)
    rota_criar_postagem(app)
    rota_excluir_postagem(app)
    rota_editar_postagem(app)
