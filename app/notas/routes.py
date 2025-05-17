
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models import Aluno, Nota
from app.forms import NotaForm

nota_bp = Blueprint('notas', __name__, url_prefix='/notas')

@nota_bp.route('/')
@login_required
def listar():
    alunos = Aluno.query.all()
    return render_template('notas/listar.html',
        titulo="Notas",
        editar_url='notas.editar',
        excluir_url='notas.excluir',
        cabecalhos=['ID', 'Nome', 'P1', 'P2', 'ATV', 'Trabalho', 'MF'],
        campos=['aluno.id', 'aluno.nome', 'p1', 'p2', 'lt', 'projeto', 'mf'],
        itens=alunos)

@nota_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    aluno = Aluno.query.get_or_404(id)
    form = NotaForm(obj=aluno.nota)
    if form.validate_on_submit():
        if aluno.nota:
            nota = aluno.nota
        else:
            nota = Nota(aluno_id=id)
            db.session.add(nota)
        nota.p1 = form.p1.data
        nota.p2 = form.p2.data
        nota.lt = form.lt.data
        nota.projeto = form.projeto.data
        nota.mf = round(nota.p1 * 0.3 + nota.p2 * 0.3 + nota.lt * 0.2 + nota.projeto * 0.2, 2)
        db.session.commit()
        flash('Notas atualizadas.')
        return redirect(url_for('notas.listar'))
