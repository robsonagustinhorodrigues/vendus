from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User

auth = Blueprint('auth', __name__)

# Rota para o login do usuário
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verificar se o usuário existe
        user = User.query.filter_by(email=email).first()

        # Depuração: Verifique se o usuário existe
        if user:
            print(f"Usuário encontrado: {user.username}")
            if user.check_password(password):  # Verificando a senha com o hash
                login_user(user)  # Registra o usuário na sessão
                return redirect(url_for('dashboard.index'))  # Redireciona para o dashboard após login
            else:
                flash('Senha incorreta. Tente novamente.', 'error')  # Mensagem de erro de senha
        else:
            flash('Usuário não encontrado. Tente novamente.', 'error')  # Mensagem de erro de usuário

    return render_template('login.html')

# Rota para o logout do usuário
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')  # Mensagem de sucesso ao deslogar
    return redirect(url_for('auth.login'))  # Redireciona de volta para a tela de login
