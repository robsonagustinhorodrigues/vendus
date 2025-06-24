# meli_ranqueamento.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import MeliIntegracao
from services.meli.meli_utils import encontrar_posicao_multiplos
from services.meli.meli_client import MeliClient
from services.meli.meli_integracao import MeliIntegracao as MeliIntegracaoService

meli_ranqueamento = Blueprint("meli_ranqueamento", __name__)

@meli_ranqueamento.route("/")
@login_required
def index():
    integracoes = MeliIntegracao.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard/meli_ranqueamento/index.html", meli_integracoes=integracoes)

@meli_ranqueamento.route("/buscar", methods=["POST"])
@login_required
def buscar():
    data = request.get_json()
    termo = data.get("termo")
    integracao_id = data.get("integracao_id")

    if not termo or not integracao_id:
        return jsonify({"status": "error", "message": "Termo e integração são obrigatórios."}), 400

    integracao = MeliIntegracao.query.filter_by(id=integracao_id, user_id=current_user.id).first()
    if not integracao:
        return jsonify({"status": "error", "message": "Integração não encontrada."}), 404

    try:
        meli_service = MeliIntegracaoService(integracao)
        mlbs = meli_service.get_mlbs_ativos()

        if not mlbs:
            return jsonify({"status": "error", "message": "Nenhum MLB ativo encontrado."}), 404

        resultado = encontrar_posicao_multiplos(
            termo, mlbs, max_paginas=20, status_callback=lambda msg: None
        )
        return jsonify({"status": "success", "data": resultado})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

