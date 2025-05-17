
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


@aluno_bp.route('/')
@login_required
def listar():
    alunos = Aluno.query.all()
    return render_template('alunos/listar.html',
        titulo="Alunos",
        novo_url='alunos.novo',
        editar_url='alunos.editar_aluno',
        excluir_url='alunos.excluir',
        cabecalhos=['ID', 'Nome', 'E-mail', 'Turma'],
        campos=['id', 'nome', 'email', 'turma_id'],
        itens=alunos)


@aluno_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = AlunoForm()
    form.turma_id.choices = [(t.id, t.nome) for t in Turma.query.all()]
    if form.validate_on_submit():
        aluno = Aluno(
            nome=form.nome.data,
            email=form.email.data,
            turma_id=form.turma_id.data
        )
        db.session.add(aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso.')
        return redirect(url_for('alunos.listar'))
    return render_template('alunos/form.html', form=form, titulo='Novo Aluno')
