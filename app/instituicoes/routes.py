from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Instituicao
from app.forms import InstituicaoForm

inst_bp = Blueprint('instituicoes', __name__, url_prefix='/instituicoes')

@inst_bp.route('/')
@login_required
def listar():
    lista = Instituicao.query.all()
    return render_template('instituicoes/listar.html',
        titulo="Instituições",
        novo_url='instituicoes.nova',
        editar_url='instituicoes.editar',
        excluir_url='instituicoes.excluir',
        cabecalhos=['ID', 'Nome', 'Sigla', 'Cidade', 'Tipo', 'Média'],
        campos=['id', 'nome', 'sigla', 'cidade', 'tipo', 'media_minima'],
        itens=lista)

@inst_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    form = InstituicaoForm()
    if form.validate_on_submit():
        inst = Instituicao(
            nome=form.nome.data,
            sigla=form.sigla.data,
            cidade=form.cidade.data,
            tipo=form.tipo.data,
            media_minima=form.media_minima.data
        )
        db.session.add(inst)
        db.session.commit()
        flash('Instituição cadastrada com sucesso.', 'success')  # Corrigido para 'success'
        return redirect(url_for('instituicoes.listar'))
    return render_template('instituicoes/form.html', form=form)

@inst_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):  # Nome simplificado
    inst = Instituicao.query.get_or_404(id)
    form = InstituicaoForm(obj=inst)
    if form.validate_on_submit():
        form.populate_obj(inst)
        db.session.commit()
        return redirect(url_for('instituicoes.listar'))
    return render_template('instituicoes/form.html', form=form, titulo='Editar Instituição')

@inst_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    inst = Instituicao.query.get_or_404(id)
    db.session.delete(inst)
    db.session.commit()
    flash('Instituição excluída.', 'warning')
    return redirect(url_for('instituicoes.listar'))