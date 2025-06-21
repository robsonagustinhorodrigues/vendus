from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import MeliIntegration
import requests

anuncios_meli = Blueprint('anuncios_meli', __name__)

# Rota principal do dashboard, mostrando os anúncios do usuário
@anuncios_meli.route('/')
@login_required
def index():
    integracoes_meli = MeliIntegration.query.filter_by(user_id=current_user.id).all()  # Pega as integrações do usuário

    # Renderiza o template e envia os anúncios para o front-end
    return render_template('dashboard.anuncios_meli.html', integracoes_meli=integracoes_meli)
