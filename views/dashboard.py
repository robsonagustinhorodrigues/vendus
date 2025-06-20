from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import MeliIntegration
import requests

dashboard = Blueprint('dashboard', __name__)

# Rota principal do dashboard, mostrando os anúncios do usuário
@dashboard.route('/')
@login_required
def index():
    meli_integrations = MeliIntegration.query.filter_by(user_id=current_user.id).all()  # Pega as integrações do usuário
    all_listings = []  # Lista que armazenará todos os anúncios

    for meli_integration in meli_integrations:
        # Requisição à API do Mercado Livre para buscar os anúncios da loja
        response = requests.get(
            f'https://api.mercadolibre.com/users/{meli_integration.mercado_livre_store_id}/items',
            headers={'Authorization': f'Bearer {meli_integration.access_token}'}
        )
        
        if response.status_code == 200:
            all_listings.append(response.json())  # Adiciona os anúncios ao array

    return render_template('dashboard.html', listings=all_listings)  # Exibe os anúncios na página

