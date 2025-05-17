
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models import Turma, Instituicao
from app.forms import TurmaForm

turma_bp = Blueprint('turmas', __name__, url_prefix='/turmas')

@turma_bp.route('/')
@login_required
def listar():
    turmas = Turma.query.all()
    return render_template('turmas/listar.html',
        titulo="Turmas",
        novo_url='turmas.novo',
        editar_url='turmas.editar',
        excluir_url='turmas.excluir',
        cabecalhos=['ID', 'Nome', 'Turno', 'Instituição'],
        campos=['id', 'nome', 'turno', 'instituicao_id'],
        itens=turmas)

@turma_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    form = TurmaForm()
    form.instituicao_id.choices = [(i.id, i.nome) for i in Instituicao.query.all()]
    if form.validate_on_submit():
        t = Turma(
            nome=form.nome.data,
            turno=form.turno.data,
            instituicao_id=form.instituicao_id.data
        )
        db.session.add(t)
        db.session.commit()
        flash('Turma cadastrada com sucesso.')
        return redirect(url_for('turmas.listar'))

@turma_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    t = Turma.query.get_or_404(id)
    form = TurmaForm(obj=t)
    form.instituicao_id.choices = [(i.id, i.nome) for i in Instituicao.query.all()]
    if form.validate_on_submit():
        t.nome = form.nome.data
        t.turno = form.turno.data
        t.instituicao_id = form.instituicao_id.data
        db.session.commit()
        flash('Turma atualizada com sucesso.')
        return redirect(url_for('turmas.listar'))

@turma_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    t = Turma.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    flash('Turma excluída.')
    return redirect(url_for('turmas.listar'))
