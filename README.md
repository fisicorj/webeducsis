
# 🎓 Sistema de Gestão Acadêmica Web

Este sistema web foi desenvolvido para permitir o controle completo de instituições de ensino, turmas, alunos, disciplinas, matrículas e notas. Ele oferece uma interface moderna e responsiva com autenticação segura e funcionalidades administrativas avançadas.

---

## 🚀 Funcionalidades

### 🔐 Autenticação
- Tela de login centralizada
- Proteção CSRF
- Hash seguro de senha

### 🏫 Instituições
- Cadastro com nome, sigla, cidade, tipo e média mínima
- Edição, exclusão e painel administrativo

### 🧑‍🏫 Turmas
- Associadas à instituição
- Cadastro, edição, exclusão e listagem

### 👨‍🎓 Alunos
- Cadastro com nome, matrícula, e-mail e telefone
- Importação por CSV
- Organização por turma

### 📚 Disciplinas
- Vinculadas a uma turma
- Cadastro, edição e exclusão

### 🧾 Matrículas
- Relacionamento N:N entre alunos e disciplinas
- Cadastro e listagem

### 📝 Notas
- Lançamento de P1, P2, atividades (LT) e trabalho
- Cálculo automático da média final (MF)
- MF colorida com base na média mínima da instituição
- Edição inline tipo planilha

---

## 🗂️ Estrutura do Banco de Dados

```
Instituicoes ──┐
               ├── Turmas ─── Disciplinas ─┐
Alunos ────────┘                         Matrículas ─── Notas
```

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11
- Flask 2.3
- SQLAlchemy
- Flask-WTF
- Bootstrap 5
- SQLite
- Gunicorn (para deploy Render)

---

## ⚙️ Instruções de Uso

### 📦 Instalação

```bash
pip install -r requirements.txt
```

### ▶️ Execução local

```bash
python run.py
```

### 🌱 Inicialização do banco de dados

```bash
python init_db.py
```

---

## 🗃️ Organização do Projeto

```
app/
├── alunos/
├── turmas/
├── instituicoes/
├── disciplinas/
├── matriculas/
├── notas/
├── templates/
├── static/
├── models.py
├── forms.py
run.py
init_db.py
requirements.txt
README.md
```

---

## 📄 Licença

Este projeto é de uso acadêmico e pode ser adaptado para fins educacionais.

---

## 👨‍💻 Autor

Sistema desenvolvido por Manoel G. Moraes com suporte da IA (OpenAI) para automação e melhorias estruturais.
