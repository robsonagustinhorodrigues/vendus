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
    return render_template('dashboard/meli_anuncios.html', meli_integracoes=meli_integracoes)


@meli_anuncios.route("/buscar", methods=["POST"])
@login_required
def buscar_anuncios():
    integracao_id = request.form.get("integracao_id")
    status = request.form.get("status")
    search = request.form.get("search")

    integracao = MeliIntegracao.query.filter_by(id=integracao_id, user_id=current_user.id).first()
    if not integracao:
        return jsonify({"status": "error", "message": "Integração não encontrada"}), 404

    try:
        meli = MeliClient(integracao)
        params = {"offset": 0, "limit": 20}
        if status:
            params["status"] = status
        if search:
            params["q"] = search

        resultado = meli.get("/users/{}/items/search".format(integracao.meli_id), params=params)

        return render_template("dashboard/meli_anuncios/resultados.html", anuncios=resultado.get("results", []))

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
