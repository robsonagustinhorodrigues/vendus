from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User  # Importando User e db do models.py

# Carregando variáveis de ambiente
load_dotenv()

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados e o login manager
db.init_app(app)  # Usando o db do models.py
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Redirecionar para a página de login se não estiver autenticado

# Função que carrega o usuário da sessão
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Criar as tabelas no banco de dados com o app context
with app.app_context():
    db.create_all()  # Cria as tabelas no banco de dados
    print("Banco de dados criado com sucesso!")

# Registrando Blueprints para as rotas de autenticação e dashboard
from views.auth import auth
from views.dashboard import dashboard
from views.api import api
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(api)

# Executando a aplicação
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
