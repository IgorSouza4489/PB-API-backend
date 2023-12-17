from flask import jsonify, request
from models import db, Usuario, Postagem
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

def configure_routes(app):
    @app.route("/usuarios")
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
        return jsonify({'usuarios': usuarios_json}), 201

    @app.route('/usuarios', methods=['POST'])
    def incluir_usuario():
        try:
            dados_usuario = request.get_json()
            data_nascimento = datetime.strptime(dados_usuario['data_nascimento'], '%d/%m/%Y').date()
            senha_hash = generate_password_hash(dados_usuario['senha'])

            novo_usuario = Usuario(
                                    nome=dados_usuario['nome'], 
                                    email=dados_usuario['email'], 
                                    data_nascimento=data_nascimento,
                                    senha=senha_hash)

            db.session.add(novo_usuario)
            db.session.commit()

            return jsonify({'mensagem': 'Usuário incluído com sucesso!'}), 201
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    @app.route("/login", methods=["POST"])
    def fazer_login():
        dados_login = request.get_json()

        if 'email' not in dados_login or 'senha' not in dados_login:
            return jsonify({'erro': 'E-mail e senha são obrigatórios.'}), 400

        email = dados_login['email']
        senha = dados_login['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            return jsonify({'mensagem': 'Sucesso'}), 200
        else:
            return jsonify({'erro': 'E-mail ou senha incorretos.'}), 401

    @app.route('/postagens', methods=['GET'])
    def obter_postagens_recentes():
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

        return jsonify({'postagens': postagens_json}), 200

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

            return jsonify({'mensagem': 'Postagem criada com sucesso!'}), 201
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    @app.route('/postagens/<int:id_postagem>', methods=['DELETE'])
    def excluir_postagem(id_postagem):
        try:
            postagem = Postagem.query.get(id_postagem)

            if postagem:
                db.session.delete(postagem)
                db.session.commit()
                return jsonify({'mensagem': 'Postagem excluída com sucesso!'}), 200
            else:
                return jsonify({'erro': 'Postagem não encontrada'}), 404

        except Exception as e:
            return jsonify({'erro': str(e)}), 500