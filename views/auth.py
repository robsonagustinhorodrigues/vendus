from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User
import requests

auth = Blueprint('auth', __name__)

# Rota para o login do usuário
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        # Verificar se o usuário existe e a senha está correta
        if user and user.check_password(password):  # Adicione a criptografia de senha mais tarde
            login_user(user)
            return redirect(url_for('dashboard.index'))  # Redireciona para o dashboard após login
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', 'error')
    return render_template('login.html')

# Rota para o logout do usuário
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  # Redireciona de volta para a tela de login

