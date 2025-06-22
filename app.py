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

# Registrando Blueprints para as rotas
from views import dashboard, api, auth, views
app.register_blueprint(views)
app.register_blueprint(dashboard)
app.register_blueprint(api)
app.register_blueprint(auth)

# Executando a aplicação
if os.getenv('FLASK_ENV') == 'development':
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        host = os.environ.get("HOST", "0.0.0.0")
        debug = os.environ.get("FLASK_ENV", "development").lower() == "development"
        app.run(host=host, port=port, debug=debug)
