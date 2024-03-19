from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    postagens = db.relationship('Postagem', backref='autor', lazy=True)

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    nome_autor = db.Column(db.String(50), nullable=False)
    datahora_postagem = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuarios_curtiram = db.relationship('Curtida', backref='postagem', lazy='dynamic')
    curtidas = db.relationship('Curtida', backref='postagem_relacionada', cascade='all, delete-orphan')

class UserApi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.created_at}')"

class Curtida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    postagem_id = db.Column(db.Integer, db.ForeignKey('postagem.id'))

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    nome_autor = db.Column(db.String(50), nullable=False)
    datahora_postagem = db.Column(db.DateTime, nullable=False)
    postagem_id = db.Column(db.Integer, db.ForeignKey('postagem.id', ondelete='CASCADE'))