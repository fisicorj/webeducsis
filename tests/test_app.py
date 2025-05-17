
import pytest
from app import create_app, db
from flask import url_for
from app.models import Usuario

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = Usuario(nome="Admin", email="admin@example.com")
            user.set_senha("123456")
            db.session.add(user)
            db.session.commit()
        yield client

def login(client):
    return client.post("/login", data=dict(email="admin@example.com", senha="123456"), follow_redirects=True)

def test_login_logout(client):
    rv = login(client)
    assert b"Painel" in rv.data or rv.status_code == 200
    rv = client.get("/logout", follow_redirects=True)
    assert b"Login" in rv.data

def test_protected_redirect(client):
    rv = client.get("/alunos/", follow_redirects=False)
    assert rv.status_code in (302, 401)

def test_create_instituicao(client):
    login(client)
    rv = client.post("/instituicoes/nova", data=dict(
        nome="IFSP", sigla="IF", cidade="São Paulo", tipo="publica", media_minima=6
    ), follow_redirects=True)
    assert b"IFSP" in rv.data
