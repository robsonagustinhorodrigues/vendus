from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import login_required, current_user

views = Blueprint('app', __name__)

from .auth import auth
from .dashboard import dashboard
from .api import api

@views.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    else:
        flash("Você precisa estar logado para acessar esta página.", "warning")
        return redirect(url_for('auth.login'))


