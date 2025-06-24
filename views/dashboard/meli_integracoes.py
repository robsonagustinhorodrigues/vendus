from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, MeliIntegracao
from services.meli.meli_client import MeliClient
from services.meli.meli_integracao import MeliIntegracao as MeliIntegracaoService

meli_integracoes = Blueprint("meli_integracoes", __name__)


@meli_integracoes.route("/")
@login_required
def index():
    meli_integracoes = MeliIntegracao.query.filter_by(user_id=current_user.id).all()

    for integracao in meli_integracoes:
        integracaoMeliService = MeliIntegracaoService(integracao)
        integracaoMeliService.update_integracao()

    meli_integracoes = MeliIntegracao.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "dashboard/meli_integracoes.html", meli_integracoes=meli_integracoes
    )


@meli_integracoes.route("/adicionar", methods=["POST"])
@login_required
def adicionar():
    meli_nome = request.form.get("nome")
    meli_store_id = request.form.get("store_id")

    if meli_nome and meli_store_id:
        meli_store_id = str(meli_store_id)
        nova = MeliIntegracao(
            meli_nome=meli_nome,
            meli_store_id=meli_store_id,
            user_id=current_user.id,
            access_token="TEMPORARIO",  # depois substitua com a autenticação real
        )
        db.session.add(nova)
        db.session.commit()
        flash("Integração adicionada com sucesso!", "success")
    else:
        flash("Preencha todos os campos.", "danger")

    return redirect(url_for("dashboard.meli_integracoes.index"))


@meli_integracoes.route("/remover", methods=["POST"])
@login_required
def remover():
    id = request.args.get("id")
    meli_integracao = MeliIntegracao.query.filter_by(id=id, user_id=current_user.id).first()

    if meli_integracao:
        db.session.delete(meli_integracao)
        db.session.commit()
        flash("Integração removida com sucesso!", "success")
    else:
        flash("Erro ao remover integração.", "danger")

    return redirect(url_for("dashboard.meli_integracoes.index"))

@meli_integracoes.route("/me/<int:id>")
@login_required
def me(id):
    meli_integracao = MeliIntegracao.query.filter_by(
        id=id, user_id=current_user.id
    ).first()
    if not meli_integracao:
        return jsonify({"status": "error", "message": "Integração não encontrada"}), 404

    try:
        meli_integracao_service = MeliIntegracaoService(meli_integracao)
        reputacao = meli_integracao_service.get_analisar_reputacao()
        if reputacao:
            return jsonify({"status": "success", "data": reputacao})
        else:
            return jsonify({"status": "error", "message": "Erro na Reposta"}), 404        

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@meli_integracoes.route("/reputacao/<int:id>")
@login_required
def reputacao(id):
    meli_integracao = MeliIntegracao.query.filter_by(
        id=id, user_id=current_user.id
    ).first()
    if not meli_integracao:
        return jsonify({"status": "error", "message": "Integração não encontrada"}), 404

    try:
        meli_client = MeliClient(meli_integracao)
        user_id = meli_integracao.meli_id

        # Dados básicos
        user_data = meli_client.get(f"users/{user_id}")
        seller_rep = user_data.get("seller_reputation", {})
        transactions = seller_rep.get("transactions", {})
        metrics = seller_rep.get("metrics", {})

        # Tentar coletar métricas de atendimento (só disponível para vendedores)
        atendimento = {}
        try:
            atendimento = meli_client.get(f"users/{user_id}/metrics")
        except Exception:
            atendimento = {}

        response_data = {
            "nickname": user_data.get("nickname", "N/D"),
            "nivel_reputacao": seller_rep.get("level_id", "N/D"),
            "status_power_seller": seller_rep.get("power_seller_status", "Não"),
            "tipo_vendedor": user_data.get("user_type", "N/D"),
            "status": user_data.get("status", {}).get("site_status", "N/D"),
            "cadastro": user_data.get("registration_date", "N/D"),
            "pontuacao": {
                "completed": transactions.get("completed", 0),
                "canceled": transactions.get("canceled", 0),
                "total": transactions.get("total", 0),
                "ratings": {
                    "positive": round(
                        transactions.get("ratings", {}).get("positive", 0) * 100, 1
                    ),
                    "negative": round(
                        transactions.get("ratings", {}).get("negative", 0) * 100, 1
                    ),
                    "neutral": round(
                        transactions.get("ratings", {}).get("neutral", 0) * 100, 1
                    ),
                },
            },
            "avaliacoes": {
                "claims": metrics.get("claims", {}).get("value", 0),
                "delayed": metrics.get("delayed_handling_time", {}).get("value", 0),
                "cancellations": metrics.get("cancellations", {}).get("value", 0),
            },
            "atendimento": {
                "taxa_resposta": atendimento.get("settings", {})
                .get("sales_channel_average_daily_messages_reply_rate", {})
                .get("value"),
                "tempo_medio": atendimento.get("settings", {})
                .get("sales_channel_average_daily_messages_delay_ms", {})
                .get("value"),
            },
        }

        return jsonify({"status": "success", "data": response_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
