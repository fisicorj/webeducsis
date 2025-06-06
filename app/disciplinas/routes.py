from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app import db
from app.models import Disciplina, Turma
from app.forms import DisciplinaForm

disciplina_bp = Blueprint('disciplinas', __name__, url_prefix='/disciplinas')

@disciplina_bp.route('/')
@login_required
def listar():
    disciplinas = Disciplina.query.all()
    return render_template('disciplinas/listar.html', disciplinas=disciplinas)

@disciplina_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    form = DisciplinaForm()
    form.turma_id.choices = [(t.id, t.nome) for t in Turma.query.all()]
    if form.validate_on_submit():
        nova = Disciplina(nome=form.nome.data, professor=form.professor.data, turma_id=form.turma_id.data)
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for('disciplinas.listar'))
    return render_template('disciplinas/form.html', form=form, titulo="Nova Disciplina")

@disciplina_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_disciplina(id):
    disc = Disciplina.query.get_or_404(id)
    form = DisciplinaForm(obj=disc)
    form.turma_id.choices = [(t.id, t.nome) for t in Turma.query.all()]
    if form.validate_on_submit():
        form.populate_obj(disc)
        db.session.commit()
        return redirect(url_for('disciplinas.listar'))
    return render_template('disciplinas/form.html', form=form, titulo="Editar Disciplina")


@disciplina_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = DisciplinasForm()
    if form.validate_on_submit():
        novo_obj = Disciplinas()
        form.populate_obj(novo_obj)
        db.session.add(novo_obj)
        db.session.commit()
        flash('Disciplinas cadastrado com sucesso.', 'success')
        return redirect(url_for('disciplinas.listar'))
    return render_template('disciplinas/form.html', form=form, titulo='Novo Disciplinas')


@disciplina_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    obj = Disciplinas.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    flash('Disciplinas excluído.', 'warning')
    return redirect(url_for('disciplinas.listar'))
