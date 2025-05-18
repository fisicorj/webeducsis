
from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Instituicao, Turma, Aluno
from app import db

painel_bp = Blueprint('painel', __name__, template_folder='templates')

@painel_bp.route('/')
@login_required
def painel():
    total_instituicoes = Instituicao.query.count()
    total_turmas = Turma.query.count()
    total_alunos = Aluno.query.count()
    return render_template('painel/index.html',
                           total_instituicoes=total_instituicoes,
                           total_turmas=total_turmas,
                           total_alunos=total_alunos)
