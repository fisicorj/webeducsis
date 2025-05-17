
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models import Aluno, Turma
from app.forms import AlunoForm

aluno_bp = Blueprint('alunos', __name__, url_prefix='/alunos')

@aluno_bp.route('/')
@login_required
def listar():
    alunos = Aluno.query.all()
        return render_template('alunos/listar.html',
            titulo="Alunos",
            novo_url='alunos.novo',
            editar_url='alunos.editar',
            excluir_url='alunos.excluir',
            cabecalhos=['ID', 'Matrícula', 'Nome', 'Email', 'Telefone', 'Turma'],
            campos=['id', 'matricula', 'nome', 'email', 'telefone', 'turma_id'],
            itens=alunos)
        titulo="Alunos",
        novo_url='alunos.novo' if hasattr(alunos_bp, 'novo') else '',
        editar_url='alunos.editar',
        excluir_url='alunos.excluir',
        cabecalhos=['ID', 'Matrícula', 'Nome', 'Email', 'Telefone', 'Turma'],
        campos=['id', 'matricula', 'nome', 'email', 'telefone', 'turma_id'],
        itens=alunos)

@aluno_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = AlunoForm()
    form.turma_id.choices = [(t.id, t.nome) for t in Turma.query.all()]
    if form.validate_on_submit():
        a = Aluno(
            matricula=form.matricula.data,
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            turma_id=form.turma_id.data
        )
        db.session.add(a)
        db.session.commit()
        flash('Aluno cadastrado com sucesso.')
        return redirect(url_for('alunos.listar'))
    return render_template('alunos/form.html', form=form)

@aluno_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    a = Aluno.query.get_or_404(id)
    form = AlunoForm(obj=a)
    form.turma_id.choices = [(t.id, t.nome) for t in Turma.query.all()]
    if form.validate_on_submit():
        a.matricula = form.matricula.data
        a.nome = form.nome.data
        a.email = form.email.data
        a.telefone = form.telefone.data
        a.turma_id = form.turma_id.data
        db.session.commit()
        flash('Aluno atualizado com sucesso.')
        return redirect(url_for('alunos.listar'))
    return render_template('alunos/form.html', form=form)

@aluno_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    a = Aluno.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('Aluno excluído.')
    return redirect(url_for('alunos.listar'))
