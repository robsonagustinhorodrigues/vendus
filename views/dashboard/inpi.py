from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import requests

inpi = Blueprint("inpi", __name__)

@inpi.route("/")
@login_required
def index():
    return render_template("dashboard/inpi/index.html")

from services.inpi_service import InpiService
@inpi.route("/consulta", methods=["POST"])
@login_required
def consulta():
    termo = request.json.get("termo")
    ncl = request.json.get("classe")  # opcional
    svc = InpiService()
    try:
        resultados = svc.buscar_marca(termo, ncl=ncl, pagina=1)
        return jsonify({"status":"success", "resultados": resultados.get("processos", [])})
    except Exception as e:
        return jsonify({"status":"error", "message": str(e)}), 500

