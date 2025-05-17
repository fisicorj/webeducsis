
from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Instituicao, Turma, Aluno, Nota
from app import db

painel_bp = Blueprint('painel', __name__)

@painel_bp.route('/')
@login_required
def painel():
    total_instituicoes = Instituicao.query.count()
    total_turmas = Turma.query.count()
    total_alunos = Aluno.query.count()
    total_notas = Nota.query.count()
    return render_template('painel.html',
                           total_instituicoes=total_instituicoes,
                           total_turmas=total_turmas,
                           total_alunos=total_alunos,
                           total_notas=total_notas)
