from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import MeliIntegration
import requests

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from .anuncios_meli import anuncios_meli
dashboard.register_blueprint(anuncios_meli, url_prefix='/anuncios_meli')

from .integracoes_meli import integracoes_meli
dashboard.register_blueprint(integracoes_meli, url_prefix='/integracoes_meli')

# Rota principal do dashboard, mostrando os anúncios do usuário
@dashboard.route('/')
@login_required
def index():
    meli_integrations = MeliIntegration.query.filter_by(user_id=current_user.id).all()  # Pega as integrações do usuário
    all_listings = []  # Lista que armazenará todos os anúncios

    # Iterar sobre todas as integrações do usuário
    for meli_integration in meli_integrations:
        try:
            # Requisição à API do Mercado Livre para buscar os anúncios da loja
            response = requests.get(
                f'https://api.mercadolibre.com/users/{meli_integration.meli_store_id}/items',
                headers={'Authorization': f'Bearer {meli_integration.access_token}'}
            )
            
            # Verifique se a requisição foi bem-sucedida
            if response.status_code == 200:
                all_listings.append(response.json())  # Adiciona os anúncios ao array
            else:
                flash(f'Erro ao carregar anúncios da API do Mercado Livre para a loja {meli_integration.meli_store_id}.', 'error')

        except requests.exceptions.RequestException as e:
            flash(f'Ocorreu um erro ao fazer a requisição para a loja {meli_integration.meli_store_id}: {e}', 'error')

    # Renderiza o template e envia os anúncios para o front-end
    return render_template('dashboard.html', listings=all_listings)
