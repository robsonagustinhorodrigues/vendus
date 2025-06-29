from flask import Blueprint, jsonify, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, MeliIntegracao
from services.meli.meli_integracao import MeliIntegracao as MeliIntegracaoService
from services.meli.meli_client import MeliClient

meli = Blueprint("meli", __name__)

from .auth import auth
meli.register_blueprint(auth, url_prefix='/auth')

@meli.route('/')
def index():
    return "API is running. api/meli"

@meli.route('/meliintegracao/<int:id>')
@login_required
def meli_integracao(id):
    meli_integracao = MeliIntegracao.query.filter_by(id=id, user_id=current_user.id).first()
    if not meli_integracao:
        return jsonify({
            "status": "error",
            "message": "Nenhuma conta Mercado Livre conectada para este usuário."
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "meli_nome": meli_integracao.meli_nome,
            "meli_id": meli_integracao.meli_id,
            "meli_email": meli_integracao.meli_email,
            "meli_link": meli_integracao.meli_link,
            "meli_store_id": meli_integracao.meli_store_id,
            "access_token": meli_integracao.access_token,
            "refresh_token": meli_integracao.refresh_token,
            "expires_at": meli_integracao.expires_at.isoformat() if meli_integracao.expires_at else None
        }
    })

@meli.route('/me/<int:id>')
@login_required
def me(id):
    meli_integracao = MeliIntegracao.query.filter_by(id=id, user_id=current_user.id).first()
    
    if not meli_integracao:
        return jsonify({
            "status": "error",
            "message": "Nenhuma integração encontrada para este ID e usuário.",
        }), 404

    meli_service = MeliIntegracaoService(meli_integracao)

    try:
        response = meli_service.get_me()
        return jsonify({
            "status": "success",
            "data": response.get("data", response),
            "raw": str(response.get("raw", {}))
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "raw": str(response.get("raw", {})) if isinstance(response, dict) else ""
        }), 500

@meli.route('/items')
@login_required
def buscar_itens():
    ids = request.args.get("ids")
    integracao_id = request.args.get("integracao_id")
    if not ids:
        return jsonify({"status": "error", "message": "IDs não informados"}), 400

    id_list = ids.split(",")

    meli_integracao = MeliIntegracao.query.filter_by(id=integracao_id, user_id=current_user.id).first()
    if not meli_integracao:
        return jsonify({"status": "error", "message": "Integração não encontrada"}), 404

    try:
        result_elements = []
        meli_client = MeliClient(meli_integracao)
        for element in id_list:
            element_response = meli_client.get(f"/items/{element}")
            result_elements.append(element_response)
            
        # print(f"Fetched {len(result_elements)} items from Mercado Livre for IDs: {id_list}")
        # print(f"Response data: {result_elements}")
        # result = meli_client.get("/items", params={"ids": ",".join(id_list)})
        return jsonify({"status": "success", "data": result_elements})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
