
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

# Executar init apenas se nenhum usuário existir
with app.app_context():
    db.create_all()
    if not User.query.first():
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso.")

if __name__ == '__main__':
    app.run()
