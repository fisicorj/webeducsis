
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.forms import LoginForm
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('painel.painel'))
        flash('Usuário ou senha inválidos')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = AuthForm()
    if form.validate_on_submit():
        novo_obj = Auth()
        form.populate_obj(novo_obj)
        db.session.add(novo_obj)
        db.session.commit()
        flash('Auth cadastrado com sucesso.')
        return redirect(url_for('auth.listar'))
    return render_template('auth/form.html', form=form, titulo='Novo Auth')


@auth_bp.route('/')
@login_required
def listar():
    itens = Auth.query.all()
    return render_template('auth/listar.html',
        titulo="Auth",
        novo_url='auth.novo',
        editar_url='auth.editar',
        excluir_url='auth.excluir',
        cabecalhos=['ID'],
        campos=['id'],
        itens=itens)


@auth_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    obj = Auth.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    flash('Auth excluído.')
    return redirect(url_for('auth.listar'))
