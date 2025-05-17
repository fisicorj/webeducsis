
from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Instituicao, Turma, Aluno, Nota
from app import db

painel_bp = Blueprint('painel', __name__)

@painel_bp.route('/')
@login_required
def painel():
    total_instituicoes = Instituicao.query.count()
    total_turmas = Turma.query.count()
    total_alunos = Aluno.query.count()
    total_notas = Nota.query.count()
    return render_template('painel.html',
                           total_instituicoes=total_instituicoes,
                           total_turmas=total_turmas,
                           total_alunos=total_alunos,
                           total_notas=total_notas)


@painel_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = PainelForm()
    if form.validate_on_submit():
        novo_obj = Painel()
        form.populate_obj(novo_obj)
        db.session.add(novo_obj)
        db.session.commit()
        flash('Painel cadastrado com sucesso.')
        return redirect(url_for('painel.listar'))
    return render_template('painel/form.html', form=form, titulo='Novo Painel')


@painel_bp.route('/')
@login_required
def listar():
    itens = Painel.query.all()
    return render_template('painel/listar.html',
        titulo="Painel",
        novo_url='painel.novo',
        editar_url='painel.editar',
        excluir_url='painel.excluir',
        cabecalhos=['ID'],
        campos=['id'],
        itens=itens)


@painel_bp.route('/excluir/<int:id>')
@login_required
def excluir(id):
    obj = Painel.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    flash('Painel excluído.')
    return redirect(url_for('painel.listar'))

from app.models import Aluno, Turma, Instituicao

@painel_bp.route('/')
@login_required
def painel():
    total_alunos = Aluno.query.count()
    total_turmas = Turma.query.count()
    total_instituicoes = Instituicao.query.count()
    return render_template('painel/painel.html',
                           total_alunos=total_alunos,
                           total_turmas=total_turmas,
                           total_instituicoes=total_instituicoes)
