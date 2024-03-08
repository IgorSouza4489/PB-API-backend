from app.controllers.usuario_controller import obter_usuarios, incluir_usuario, fazer_login
from app.controllers.postagem_controller import obter_postagens, criar_postagem, excluir_postagem, editar_postagem
from app.controllers.curtida_controller import adicionar_curtida
from app.controllers.auth_controller import registrar_usuario_api, fazer_login_api


def configure_routes(app):
    app.route("/usuarios", methods=['GET'])(obter_usuarios)

    app.route('/usuarios', methods=['POST'])(incluir_usuario)

    app.route("/login", methods=["POST"])(fazer_login)

    app.route('/postagens', methods=['GET'])(obter_postagens)

    app.route('/postagens', methods=['POST'])(criar_postagem)

    app.route('/postagens/<int:id_postagem>', methods=['DELETE'])(excluir_postagem)

    app.route('/postagens/<int:id_postagem>', methods=['PUT'])(editar_postagem)

    app.route('/postagens/<int:id_postagem>/curtidas', methods=['POST'])(adicionar_curtida)

    #Auth API
    app.route("/registro_api", methods=['POST'])(registrar_usuario_api)

    app.route("/login_api", methods=["POST"])(fazer_login_api)