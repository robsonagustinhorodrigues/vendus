from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import requests

inpi = Blueprint("inpi", __name__)

@inpi.route("/")
@login_required
def index():
    return render_template("dashboard/inpi/index.html")

@inpi.route("/consulta", methods=["POST"])
@login_required
def consulta():
    termo = request.json.get("termo")
    if not termo:
        return jsonify({"status": "error", "message": "Informe um termo para buscar."})

    try:
        # Exemplo de scraping ou API pública do INPI (usar requests, selenium ou biblioteca própria)
        # Aqui é simulado com retorno fixo
        resultados = [
            {"marca": termo.upper(), "situacao": "Registrada", "processo": "920341200"},
            {"marca": termo.upper() + " PRO", "situacao": "Pedido", "processo": "930421873"}
        ]
        return jsonify({"status": "success", "resultados": resultados})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
