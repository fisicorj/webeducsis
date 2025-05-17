
from app import db
from flask_login import UserMixin
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Instituicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(50))
    tipo = db.Column(db.String(10))
    media_minima = db.Column(db.Float, default=6.0)
    turmas = db.relationship('Turma', backref='instituicao', lazy=True)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turno = db.Column(db.String(20))
    instituicao_id = db.Column(db.Integer, db.ForeignKey('instituicao.id'), nullable=False)
    alunos = db.relationship('Aluno', backref='turma', lazy=True)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    nota = db.relationship('Nota', backref='aluno', uselist=False)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    p1 = db.Column(db.Float)
    p2 = db.Column(db.Float)
    lt = db.Column(db.Float)
    projeto = db.Column(db.Float)
    mf = db.Column(db.Float)
