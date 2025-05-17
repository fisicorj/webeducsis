
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'
DATABASE = 'controle_turma_final.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('listar_alunos'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        db = get_db()
        user_record = db.execute('SELECT * FROM usuarios WHERE username=? AND password=?', (user, pwd)).fetchone()
        if user_record:
            session['user'] = user
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/instituicoes', methods=['GET', 'POST'])
def instituicoes():
    db = get_db()
    if request.method == 'POST':
        nome = request.form['nome']
        sigla = request.form['sigla']
        cidade = request.form['cidade']
        tipo = request.form['tipo']
        db.execute('INSERT INTO instituicoes (nome, sigla, cidade, tipo) VALUES (?, ?, ?, ?)', (nome, sigla, cidade, tipo))
        db.commit()
    insts = db.execute('SELECT * FROM instituicoes').fetchall()
    return render_template('instituicoes.html', instituicoes=insts)

@app.route('/turmas', methods=['GET', 'POST'])
def turmas():
    db = get_db()
    if request.method == 'POST':
        nome = request.form['nome']
        turno = request.form['turno']
        instituicao_id = request.form['instituicao_id']
        db.execute('INSERT INTO turmas (nome, turno, instituicao_id) VALUES (?, ?, ?)', (nome, turno, instituicao_id))
        db.commit()
    turmas = db.execute('SELECT t.*, i.nome AS inst_nome FROM turmas t JOIN instituicoes i ON t.instituicao_id = i.id').fetchall()
    instituicoes = db.execute('SELECT * FROM instituicoes').fetchall()
    return render_template('turmas.html', turmas=turmas, instituicoes=instituicoes)

@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    db = get_db()
    if request.method == 'POST':
        matricula = request.form['matricula']
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        turma_id = request.form['turma_id']
        db.execute('INSERT INTO alunos (matricula, nome, email, telefone, turma_id) VALUES (?, ?, ?, ?, ?)', (matricula, nome, email, telefone, turma_id))
        db.commit()
    alunos = db.execute('SELECT a.*, t.nome AS turma_nome FROM alunos a JOIN turmas t ON a.turma_id = t.id').fetchall()
    turmas = db.execute('SELECT * FROM turmas').fetchall()
    return render_template('alunos.html', alunos=alunos, turmas=turmas)

@app.route('/notas/<int:id_aluno>', methods=['GET', 'POST'])
def notas(id_aluno):
    db = get_db()
    aluno = db.execute('SELECT * FROM alunos WHERE id = ?', (id_aluno,)).fetchone()
    if request.method == 'POST':
        p1 = float(request.form['p1'])
        p2 = float(request.form['p2'])
        lt = float(request.form['lt'])
        projeto = float(request.form['projeto'])
        mf = round(0.3*p1 + 0.3*p2 + 0.2*lt + 0.2*projeto, 2)
        db.execute('REPLACE INTO notas_finais (id_aluno, p1, p2, lt, projeto, mf) VALUES (?, ?, ?, ?, ?, ?)',
                   (id_aluno, p1, p2, lt, projeto, mf))
        db.commit()
        return redirect(url_for('listar_alunos'))
    nota = db.execute('SELECT * FROM notas_finais WHERE id_aluno = ?', (id_aluno,)).fetchone()
    return render_template('notas.html', aluno=aluno, nota=nota)

@app.route('/listar_alunos')
def listar_alunos():
    db = get_db()
    query = '''
    
    SELECT a.id as id, a.matricula, a.nome, a.email, a.telefone, t.nome AS turma,
           n.p1, n.p2, n.lt, n.projeto, n.mf
    FROM alunos a
    JOIN turmas t ON a.turma_id = t.id
    LEFT JOIN notas_finais n ON a.id = n.id_aluno
    
           n.p1, n.p2, n.lt, n.projeto, n.mf
    FROM alunos a
    JOIN turmas t ON a.turma_id = t.id
    LEFT JOIN notas_finais n ON a.id = n.id_aluno
    '''
    alunos = db.execute(query).fetchall()
    return render_template('grid_notas.html', alunos=alunos)


@app.route('/painel')
def painel():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    total_instituicoes = db.execute('SELECT COUNT(*) FROM instituicoes').fetchone()[0]
    total_turmas = db.execute('SELECT COUNT(*) FROM turmas').fetchone()[0]
    total_alunos = db.execute('SELECT COUNT(*) FROM alunos').fetchone()[0]
    total_notas = db.execute('SELECT COUNT(*) FROM notas_finais').fetchone()[0]
    return render_template('painel.html', 
                           total_instituicoes=total_instituicoes,
                           total_turmas=total_turmas,
                           total_alunos=total_alunos,
                           total_notas=total_notas)


if __name__ == '__main__':
    app.run(debug=True)
