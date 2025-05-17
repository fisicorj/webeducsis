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
