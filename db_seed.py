from app import app, db
from models import User
from werkzeug.security import generate_password_hash

# Usando o contexto da aplicação para interagir com o banco de dados
with app.app_context():
    # Criando usuários fictícios
    user1 = User(username='Robson', email='robson@ortopasso.com.br', password=generate_password_hash('Master32'))

    # Adicionando os usuários à sessão
    db.session.add(user1)

    # Comitando as alterações no banco de dados
    db.session.commit()

    print("Usuários criados com sucesso!")
