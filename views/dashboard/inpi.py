# inpi.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from services.inpi_service import InpiService

inpi = Blueprint("inpi", __name__)

@inpi.route("/dashboard/inpi")
@login_required
def index():
    return render_template("dashboard/inpi/index.html")

@inpi.route("/dashboard/inpi/consulta", methods=["POST"])
@login_required
def consulta():
    print("🔍 Iniciando consulta INPI")
    data = request.get_json()
    termo = data.get("termo", "").strip()
    pagina = int(data.get("pagina", 1))

    if not termo:
        print("⚠️ Termo de busca não informado.")
        return jsonify({"status": "error", "message": "Termo não informado."}), 400

    try:
        print(f"🔍 Buscando marcas para o termo: {termo} (página {pagina})")
        service = InpiService()
        resultados = service.buscar_marcas(termo, pagina)
        
        return jsonify({"status": "success", "dados": resultados})
    except Exception as e:
        print(f"❌ Erro ao buscar marcas: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@inpi.route("/dashboard/inpi/detalhes", methods=["POST"])
@login_required
def detalhes():
    data = request.get_json()
    link = data.get("link", "")

    if not link:
        return jsonify({"status": "error", "message": "Link não informado."}), 400

    try:
        service = InpiService()
        detalhes = service.detalhes_marca(link)
        return jsonify({"status": "success", "dados": detalhes})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
