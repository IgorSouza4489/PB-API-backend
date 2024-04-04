from app.controllers.usuario_controller import obter_usuarios, incluir_usuario, fazer_login, obter_usuario_id
from app.controllers.postagem_controller import obter_postagens, criar_postagem, excluir_postagem, editar_postagem, adicionar_comentario, get_comentarios_por_postagem
from app.controllers.curtida_controller import adicionar_curtida, obter_curtidas, obter_postagens_mais_curtidas, obter_postagens_curtidas_mim
from app.controllers.auth_controller import registrar_usuario_api, fazer_login_api


def configure_routes(app):
    app.route("/usuarios", methods=['GET'])(obter_usuarios)

    app.route("/obter_usuarios", methods=['GET'])(obter_usuario_id)

    app.route('/usuarios', methods=['POST'])(incluir_usuario)

    app.route("/login", methods=["POST"])(fazer_login)

    app.route('/postagens', methods=['GET'])(obter_postagens)

    app.route('/postagens', methods=['POST'])(criar_postagem)
    app.route('/adicionar-comentario/<int:id_postagem>', methods=['POST'])(adicionar_comentario)
    app.route('/buscar-comentario/<int:id_postagem>', methods=['GET'])(get_comentarios_por_postagem)


    app.route('/postagens/<int:id_postagem>', methods=['DELETE'])(excluir_postagem)

    app.route('/postagens/<int:id_postagem>', methods=['PATCH'])(editar_postagem)

    app.route('/postagens/curtidas/<int:id_postagem>', methods=['POST'])(adicionar_curtida)

    app.route('/postagens-curtidas-mim', methods=['GET'])(obter_postagens_curtidas_mim)

    app.route('/postagens-mais-curtidas', methods=['GET'])(obter_postagens_mais_curtidas)

    app.route('/postagens/curtidas/<int:id_postagem>', methods=['GET'])(obter_curtidas)

    #Auth API
    app.route("/registro_api", methods=['POST'])(registrar_usuario_api)

    app.route("/login_api", methods=["POST"])(fazer_login_api)