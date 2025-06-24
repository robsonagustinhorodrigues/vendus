from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

# Rota para o login do usuário
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Você já está logado!', 'info')
        return redirect(url_for('dashboard.index'))
    
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

    return render_template('auth/login.html')

# Rota para o logout do usuário
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')  # Mensagem de sucesso ao deslogar
    return redirect(url_for('auth.login'))  # Redireciona de volta para a tela de login

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Você já está logado!', 'info')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        codigo = request.form.get('codigo').strip()

        # Validações
        if not username or not email or not password or not confirm_password:
            return render_template('auth/register.html', error="Todos os campos são obrigatórios.")
        
        if password != confirm_password:
            return render_template('auth/register.html', error="As senhas não coincidem.")
        
        if codigo.lower() != "faça o simples":
            return render_template('auth/register.html', error="Código de convite inválido.")

        # Verifica se usuário já existe
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return render_template('auth/register.html', error="Usuário ou e-mail já registrado.")

        # Cria o novo usuário
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')
