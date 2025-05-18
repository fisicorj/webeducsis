from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Aluno, Turma, Instituicao, Matricula
from app import db

painel_bp = Blueprint('painel', __name__, url_prefix='/painel')

@painel_bp.route('/')
@login_required
def painel():
    total_alunos = Aluno.query.count()
    total_turmas = Turma.query.count()
    total_instituicoes = Instituicao.query.count()
    total_matriculas = Matricula.query.count()

    # Distribuição de alunos por turma
    dados = db.session.query(Turma.nome, db.func.count(Aluno.id))        .join(Aluno, Aluno.turma_id == Turma.id)        .group_by(Turma.nome)        .all()

    labels = [nome for nome, _ in dados]
    data = [total for _, total in dados]

    return render_template('painel/painel.html',
        total_alunos=total_alunos,
        total_turmas=total_turmas,
        total_instituicoes=total_instituicoes,
        total_matriculas=total_matriculas,
        labels=labels,
        data=data)