
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models import Instituicao
from app.forms import InstituicaoForm

inst_bp = Blueprint('instituicoes', __name__, url_prefix='/instituicoes')

@inst_bp.route('/')
@login_required
def listar():
    lista = Instituicao.query.all()
    return render_template('instituicoes/listar.html', instituicoes=lista)

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
        flash('Instituição cadastrada com sucesso.')
        return redirect(url_for('instituicoes.listar'))
    return render_template('instituicoes/form.html', form=form)

@inst_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    inst = Instituicao.query.get_or_404(id)
    form = InstituicaoForm(obj=inst)
    if form.validate_on_submit():
        inst.nome = form.nome.data
        inst.sigla = form.sigla.data
        inst.cidade = form.cidade.data
        inst.tipo = form.tipo.data
        inst.media_minima = form.media_minima.data
        db.session.commit()
        flash('Instituição atualizada com sucesso.')
        return redirect(url_for('instituicoes.listar'))
    return render_template('instituicoes/form.html', form=form)

@inst_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    inst = Instituicao.query.get_or_404(id)
    db.session.delete(inst)
    db.session.commit()
    flash('Instituição excluída.')
    return redirect(url_for('instituicoes.listar'))
