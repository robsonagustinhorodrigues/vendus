from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    meli_integrations = db.relationship('MeliIntegration', backref='user', lazy=True)
    
    # Função para definir a senha com hash
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Função para verificar a senha
    def check_password(self, password):
        return check_password_hash(self.password, password)

class MeliIntegration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meli_nome = db.Column(db.String(255), nullable=True)
    meli_id = db.Column(db.String(255), nullable=True)
    meli_email = db.Column(db.String(255), nullable=True)
    meli_link = db.Column(db.String(255), nullable=True)
    meli_store_id = db.Column(db.String(255), nullable=True)
    access_token = db.Column(db.String(255), nullable=True)
    refresh_token = db.Column(db.String(255), nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
