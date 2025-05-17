
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'super_secret'

DATABASE = 'controle_turma_manha_v2.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    alunos = db.execute('SELECT * FROM alunos').fetchall()
    return render_template('index.html', alunos=alunos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        db = get_db()
        result = db.execute('SELECT * FROM usuarios WHERE username=? AND password=?', (user, pwd)).fetchone()
        if result:
            session['user'] = user
            return redirect(url_for('index'))
        flash('Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/cadastrar-aluno', methods=['GET', 'POST'])
def cadastrar_aluno():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        id_aluno = request.form['id_aluno']
        nome = request.form['nome']
        db = get_db()
        db.execute('INSERT INTO alunos (id_aluno, nome) VALUES (?, ?)', (id_aluno, nome))
        db.commit()
        return redirect(url_for('index'))
    return render_template('cadastrar.html')

@app.route('/importar-alunos', methods=['GET', 'POST'])
def importar_alunos():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        f = request.files['file']
        if f:
            df = pd.read_csv(f)
            db = get_db()
            for _, row in df.iterrows():
                db.execute('INSERT OR IGNORE INTO alunos (id_aluno, nome) VALUES (?, ?)', (row['id_aluno'], row['nome']))
            db.commit()
            return redirect(url_for('index'))
    return render_template('importar.html')

@app.route('/editar-notas/<id_aluno>', methods=['GET', 'POST'])
def editar_notas(id_aluno):
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        p1 = request.form['p1']
        p2 = request.form['p2']
        lt = request.form['lt']
        projeto = request.form['projeto']
        mf = request.form['mf']
        db.execute('REPLACE INTO notas_finais (id_aluno, p1, p2, lt, projeto, mf) VALUES (?, ?, ?, ?, ?, ?)',
                   (id_aluno, p1, p2, lt, projeto, mf))
        db.commit()
        return redirect(url_for('index'))
    notas = db.execute('SELECT * FROM notas_finais WHERE id_aluno = ?', (id_aluno,)).fetchone()
    aluno = db.execute('SELECT * FROM alunos WHERE id_aluno = ?', (id_aluno,)).fetchone()
    return render_template('editar.html', aluno=aluno, notas=notas)

if __name__ == '__main__':
    app.run(debug=True)
