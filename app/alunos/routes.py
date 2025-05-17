
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models import Aluno, Turma
from app.forms import AlunoForm

aluno_bp = Blueprint('alunos', __name__, url_prefix='/alunos')

@aluno_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    form = AlunoForm(obj=aluno)
    if form.validate_on_submit():
        form.populate_obj(aluno)
        db.session.commit()
        return redirect(url_for('alunos.listar'))
    return render_template('alunos/form.html', form=form, titulo='Editar Aluno')

@aluno_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    a = Aluno.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('Aluno excluído.')
    return redirect(url_for('alunos.listar'))
