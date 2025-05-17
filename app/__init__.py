from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():


    def utility_processor():
        return dict(getattr=getattr)

    app = Flask(__name__)

    @app.context_processor
    def utility_processor():
        return dict(getattr=getattr)
    app.config['SECRET_KEY'] = 'segredo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///controle.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.auth.routes import auth_bp
    from app.instituicoes.routes import inst_bp
    from app.turmas.routes import turma_bp
    from app.alunos.routes import aluno_bp
    from app.notas.routes import nota_bp
    from app.painel.routes import painel_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inst_bp)
    app.register_blueprint(turma_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(painel_bp)

    return app
