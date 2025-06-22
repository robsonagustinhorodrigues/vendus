from app import app, db
from models import User
from werkzeug.security import generate_password_hash

# Usando o contexto da aplicação para interagir com o banco de dados
with app.app_context():
    # Cria as tabelas se ainda não existirem
    db.create_all()

    # Verifica se já existe um usuário com o mesmo e-mail
    existing_user = User.query.filter_by(email='admin@admin.com').first()
    if existing_user:
        print("Usuário admin@admin.com já existe.")
    else:
        # Criando usuário fictício
        user1 = User(username='Admin', email='admin@admin.com')
        user1.set_password('admin123')  
        db.session.add(user1)
        db.session.commit()
        print("Usuário criado com sucesso!")
