
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models import Aluno, Nota
from app.forms import NotaForm

nota_bp = Blueprint('notas', __name__, url_prefix='/notas')

@nota_bp.route('/')
@login_required
@nota_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@nota_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_nota(id):
    nota = Nota.query.get_or_404(id)
    form = NotaForm(obj=nota)
    if form.validate_on_submit():
        form.populate_obj(nota)
        nota.mf = round(nota.p1 * 0.3 + nota.p2 * 0.3 + nota.lt * 0.2 + nota.projeto * 0.2, 1)
        db.session.commit()
        return redirect(url_for('notas.listar'))
    return render_template('notas/form.html', form=form, titulo='Editar Nota')

@nota_bp.route('/')
@login_required
def listar():
    alunos = Aluno.query.all()
    itens = []
    for aluno in alunos:
        nota = aluno.nota
        itens.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "p1": nota.p1,
            "p2": nota.p2,
            "lt": nota.lt,
            "projeto": nota.projeto,
            "mf": nota.mf
        })
        aluno_dict = {
            'media_minima': aluno.turma.instituicao.media_minima if aluno.turma and aluno.turma.instituicao else 6.0
        }
    return render_template('notas/listar.html',
        titulo="Notas",
        cabecalhos=["ID", "Nome", "P1", "P2", "ATV", "Trabalho", "MF"],
        campos=["id", "nome", "p1", "p2", "lt", "projeto", "mf"],
        itens=itens)


@nota_bp.route('/atualizar', methods=['POST'])
@login_required
def atualizar():
    ids = request.form.getlist('atualizar_ids')
    for id_str in ids:
        try:
            id = int(id_str)
            nota = Nota.query.join(Aluno).filter(Aluno.id == id).first()
            nota.p2 = float(request.form.get(f"p2_{id}"))
            nota.lt = float(request.form.get(f"lt_{id}"))
            nota.projeto = float(request.form.get(f"projeto_{id}"))
            nota.mf = round(nota.p1 * 0.3 + nota.p2 * 0.3 + nota.lt * 0.2 + nota.projeto * 0.2, 1)
        except:
            continue
    db.session.commit()
    return redirect(url_for('notas.listar'))
