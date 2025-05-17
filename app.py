from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo'
DATABASE = 'controle_turma_manha.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def calcular_mf(p1, p2, atv, trab):
    return round(p1 * 0.3 + p2 * 0.3 + atv * 0.2 + trab * 0.2, 2)

@app.route('/', methods=['GET'])
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
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    db = get_db()
    aluno = db.execute('SELECT * FROM alunos WHERE id_aluno=?', (id,)).fetchone()
    nota = db.execute('SELECT * FROM notas_finais WHERE id_aluno=?', (id,)).fetchone()
    if request.method == 'POST':
        p1 = float(request.form['p1'])
        p2 = float(request.form['p2'])
        atv = float(request.form['lt'])
        trab = float(request.form['projeto'])
        mf = calcular_mf(p1, p2, atv, trab)
        db.execute('REPLACE INTO notas_finais VALUES (?, ?, ?, ?, ?, ?)', (id, p1, p2, atv, trab, mf))
        db.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', aluno=aluno, nota=nota)

if __name__ == '__main__':
    app.run(debug=True)