from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import MeliIntegracao
import requests

meli_anuncios = Blueprint('meli_anuncios', __name__)

# Rota principal do dashboard, mostrando os anúncios do usuário
@meli_anuncios.route('/')
@login_required
def index():
    meli_integracoes = MeliIntegracao.query.filter_by(user_id=current_user.id).all()  # Pega as integrações do usuário

    # Renderiza o template e envia os anúncios para o front-end
    return render_template('dashboard/meli_anuncios.html', meli_integracoes=meli_integracoes)
