from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'controle_turma_manha.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM alunos')
    alunos = cur.fetchall()
    return render_template('index.html', alunos=alunos)

@app.route('/aluno/<id_aluno>')
def aluno(id_aluno):
    db = get_db()
    aluno = db.execute('SELECT * FROM alunos WHERE id_aluno = ?', (id_aluno,)).fetchone()
    notas = db.execute('SELECT * FROM notas_finais WHERE id_aluno = ?', (id_aluno,)).fetchone()
    provas = db.execute('SELECT * FROM provas WHERE id_aluno = ?', (id_aluno,)).fetchone()
    atividades = db.execute('SELECT * FROM atividades WHERE id_aluno = ?', (id_aluno,)).fetchone()
    projeto = db.execute('SELECT * FROM projetos WHERE id_aluno = ?', (id_aluno,)).fetchone()
    return render_template('aluno.html', aluno=aluno, notas=notas, provas=provas, atividades=atividades, projeto=projeto)

if __name__ == '__main__':
    app.run(debug=True)
