
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave'
DATABASE = 'controle_turma_integrado.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    query = '''
        SELECT a.matricula, a.nome, a.email, a.telefone, t.nome AS turma, n.p1, n.p2, n.lt, n.projeto, n.mf
        FROM alunos a
        JOIN turmas t ON a.turma_id = t.id
        LEFT JOIN notas_finais n ON a.id = n.id_aluno
    '''
    alunos = db.execute(query).fetchall()
    return render_template('alunos_notas.html', alunos=alunos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        db = get_db()
        result = db.execute('SELECT * FROM usuarios WHERE username=? AND password=?', (u, p)).fetchone()
        if result:
            session['user'] = u
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
