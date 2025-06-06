from datetime import datetime


class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    professor = db.Column(db.String(100))
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    turma = db.relationship('Turma', backref=db.backref('disciplinas', lazy=True))

# No arquivo models.py
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(
        db.String(20), 
        nullable=False, 
        unique=True, 
        default=lambda: str(int(datetime.now().timestamp()))  # Geração automática
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'))
    
    turma = db.relationship('Turma', back_populates='alunos')
    
class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    aluno = db.relationship('Aluno', backref=db.backref('matriculas', lazy=True))
    disciplina = db.relationship('Disciplina', backref=db.backref('matriculas', lazy=True))
    __table_args__ = (db.UniqueConstraint('aluno_id', 'disciplina_id', name='_aluno_disciplina_uc'),)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matricula.id'), nullable=False)
    p1 = db.Column(db.Float, default=0)
    p2 = db.Column(db.Float, default=0)
    lt = db.Column(db.Float, default=0)
    projeto = db.Column(db.Float, default=0)
    mf = db.Column(db.Float, default=0)
    matricula = db.relationship('Matricula', backref=db.backref('nota', uselist=False))

from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
