from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import MeliIntegracao
import requests

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from .meli_anuncios import meli_anuncios
dashboard.register_blueprint(meli_anuncios, url_prefix='/meli_anuncios')

from .meli_integracoes import meli_integracoes
dashboard.register_blueprint(meli_integracoes, url_prefix='/meli_integracoes')

from .meli_ranqueamento import meli_ranqueamento
dashboard.register_blueprint(meli_ranqueamento, url_prefix='/meli_ranqueamento')

from .inpi import inpi
dashboard.register_blueprint(inpi, url_prefix='/inpi')

# Rota principal do dashboard, mostrando os anúncios do usuário
@dashboard.route('/')
@login_required
def index():
    meli_integracoes = MeliIntegracao.query.filter_by(user_id=current_user.id).all()  # Pega as integrações do usuário
    all_listings = []  # Lista que armazenará todos os anúncios

    # Iterar sobre todas as integrações do usuário
    for meli_integracao in meli_integracoes:
        try:
            # Requisição à API do Mercado Livre para buscar os anúncios da loja
            response = requests.get(
                f'https://api.mercadolibre.com/users/{meli_integracao.meli_store_id}/items',
                headers={'Authorization': f'Bearer {meli_integracao.access_token}'}
            )
            
            # Verifique se a requisição foi bem-sucedida
            if response.status_code == 200:
                all_listings.append(response.json())  # Adiciona os anúncios ao array
            else:
                flash(f'Erro ao carregar anúncios da API do Mercado Livre para a loja {meli_integracao.meli_store_id}.', 'error')

        except requests.exceptions.RequestException as e:
            flash(f'Ocorreu um erro ao fazer a requisição para a loja {meli_integracao.meli_store_id}: {e}', 'error')

    # Renderiza o template e envia os anúncios para o front-end
    return render_template('dashboard.html', listings=all_listings)
