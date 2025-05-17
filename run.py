from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

# Executa somente se o banco ainda estiver vazio
with app.app_context():
    db.create_all()
    if not User.query.first():
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado.")

if __name__ == '__main__':
    app.run()

