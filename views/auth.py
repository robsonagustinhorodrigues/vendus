from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User

auth = Blueprint('auth', __name__)

# Rota para o login do usuário
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Verificar se o usuário já está logado
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))  # Redireciona para o dashboard se já estiver logado

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar se o usuário existe
        user = User.query.filter_by(username=username).first()
        
        # Verificar se o usuário existe e se a senha está correta
        if user and user.check_password(password):  # Usando o método de verificação de senha
            login_user(user)  # Registra o usuário na sessão
            return redirect(url_for('dashboard.index'))  # Redireciona para o dashboard após login
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', 'error')  # Exibe mensagem de erro

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Faz o logout do usuário
    flash('Você foi desconectado com sucesso!', 'success')  # Mensagem de sucesso ao deslogar
    return redirect(url_for('auth.login')) 
