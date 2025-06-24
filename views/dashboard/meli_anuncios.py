from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import MeliIntegracao
from services.meli.meli_client import MeliClient

meli_anuncios = Blueprint('meli_anuncios', __name__)

# Rota principal do dashboard, mostrando os anúncios do usuário
@meli_anuncios.route('/')
@login_required
def index():
    meli_integracoes = MeliIntegracao.query.filter_by(user_id=current_user.id).all()  # Pega as integrações do usuário

    # Renderiza o template e envia os anúncios para o front-end
    return render_template('dashboard/meli_anuncios/index.html', meli_integracoes=meli_integracoes)


@meli_anuncios.route('/buscar', methods=['POST'])
@login_required
def buscar():
    integracao_id = request.form.get("integracao_id")
    q = request.form.get("q")
    status = request.form.get("status")
    offset = request.form.get("offset", type=int, default=0)
    limit = request.form.get("limit", type=int, default=50)

    meli_integracao = MeliIntegracao.query.filter_by(id=integracao_id, user_id=current_user.id).first()
    if not meli_integracao:
        return jsonify({"status": "error", "message": "Integração não encontrada"}), 404

    try:
        meli = MeliClient(meli_integracao)

        params = {
            "offset": offset,
            "limit": limit
        }
        if q: params["q"] = q
        if status: params["status"] = status

        seller_id = meli_integracao.meli_store_id  # Corrigido
        response = meli.get(f"/users/{seller_id}/items/search", params=params)

        return jsonify({"status": "success", "data": response})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

