
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    admin = User(username='admin', password=generate_password_hash('admin123'))
    db.session.add(admin)
    db.session.commit()
    print("Banco de dados criado e usuário admin gerado.")
