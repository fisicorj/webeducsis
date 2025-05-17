from app import create_app, db
from app.models import Instituicao, Turma, Aluno, Nota
from werkzeug.security import generate_password_hash
import random

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

# Criar instituições
inst1 = Instituicao(nome="Universidade Alpha", sigla="UA", cidade="São Paulo", tipo="Pública", media_minima=6.0)
inst2 = Instituicao(nome="Instituto Beta", sigla="IB", cidade="Rio de Janeiro", tipo="Privada", media_minima=7.0)
db.session.add_all([inst1, inst2])
db.session.commit()

# Criar turmas
turma1 = Turma(nome="TADS-M1", turno="Manhã", instituicao_id=inst1.id)
turma2 = Turma(nome="TADS-N1", turno="Noite", instituicao_id=inst2.id)
db.session.add_all([turma1, turma2])
db.session.commit()

# Gerar alunos e notas
nomes = [
    "Ana Souza", "Carlos Pereira", "Beatriz Lima", "Diego Silva", "Eduarda Ramos",
    "Fábio Castro", "Gabriela Nunes", "Henrique Teixeira", "Isabela Rocha", "João Vitor",
    "Karen Almeida", "Lucas Dias", "Marina Costa", "Natália Freitas", "Otávio Mendes",
    "Paula Borges", "Ricardo Leal", "Sabrina Lopes", "Thiago Duarte", "Vanessa Pinto"
]

for i, nome in enumerate(nomes):
    email = nome.lower().replace(" ", ".") + "@email.com"
    telefone = f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    turma = turma1 if i < 10 else turma2
    aluno = Aluno(matricula=f"2024{i+1:03}", nome=nome, email=email, telefone=telefone, turma_id=turma.id)
    db.session.add(aluno)
    db.session.flush()  # pegar ID

    p1 = round(random.uniform(4, 9), 1)
    p2 = round(random.uniform(4, 9), 1)
    atv = round(random.uniform(5, 10), 1)
    trab = round(random.uniform(5, 10), 1)
    mf = round(p1 * 0.3 + p2 * 0.3 + atv * 0.2 + trab * 0.2, 1)

    nota = Nota(aluno_id=aluno.id, p1=p1, p2=p2, lt=atv, projeto=trab, mf=mf)
    db.session.add(nota)

db.session.commit()
print("Base de dados populada com sucesso!")
