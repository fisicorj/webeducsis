from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Matricula, Aluno, Disciplina
from app.forms import MatriculaForm

matricula_bp = Blueprint('matriculas', __name__, url_prefix='/matriculas')

@matricula_bp.route('/')
@login_required
def listar():
    matriculas = Matricula.query.all()
    return render_template('matriculas/listar.html', matriculas=matriculas)

@matricula_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    form = MatriculaForm()
    form.aluno_id.choices = [(a.id, a.nome) for a in Aluno.query.all()]
    form.disciplina_id.choices = [(d.id, d.nome) for d in Disciplina.query.all()]
    if form.validate_on_submit():
        m = Matricula(aluno_id=form.aluno_id.data, disciplina_id=form.disciplina_id.data)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('matriculas.listar'))
    return render_template('matriculas/form.html', form=form, titulo="Nova Matrícula")


@matricula_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = MatriculasForm()
    if form.validate_on_submit():
        novo_obj = Matriculas()
        form.populate_obj(novo_obj)
        db.session.add(novo_obj)
        db.session.commit()
        flash('Matriculas cadastrado com sucesso.')
        return redirect(url_for('matriculas.listar'))
    return render_template('matriculas/form.html', form=form, titulo='Novo Matriculas')


@matricula_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    obj = Matriculas.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    flash('Matriculas excluído.')
    return redirect(url_for('matriculas.listar'))
