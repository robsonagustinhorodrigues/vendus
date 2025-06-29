import os
import requests
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import login_required, current_user
from models import db, MeliIntegracao
import os
import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from services.meli.meli_client import MeliClient

auth = Blueprint("auth", __name__)

@auth.route("/")
def index():
    return "API is running. api/meli/auth"

@auth.route("/login")
@login_required
def iniciar_login_meli():
    code_verifier = secrets.token_urlsafe(48)[:64]
    sha256_hash = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_hash).decode().rstrip("=")

    session["meli_code_verifier"] = code_verifier
    client_id = os.getenv("MELI_CLIENT_ID", "")
    redirect_uri = os.getenv("MELI_REDIRECT_URI", "")
    user_id = current_user.id

    meli_auth_url = (
        f"https://auth.mercadolivre.com.br/authorization?"
        f"state={user_id}&response_type=code&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&code_challenge={code_challenge}&code_challenge_method=S256"
    )
    return redirect(meli_auth_url)


@auth.route("/callback")
@login_required
def callback_meli():

    state = request.args.get("state")
    code = request.args.get("code")

    if not code:
        flash("Código de autorização não recebido.", "danger")
        return redirect(url_for("dashboard.meli_integracoes.index"))

    code_verifier = session.get("meli_code_verifier")
    if not code_verifier:
        flash("Code Verifier não encontrado na sessão.", "danger")
        return redirect(url_for("dashboard.meli_integracoes.index"))

    token_url = os.getenv("MELI_URL_TOKEN", "https://api.mercadolibre.com/oauth/token")
    payload = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("MELI_CLIENT_ID"),
        "client_secret": os.getenv("MELI_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.getenv("MELI_REDIRECT_URI"),
        "code_verifier": code_verifier,
    }

    response = requests.post(
        token_url, data=payload, headers={"Accept": "application/json"}
    )
    if response.status_code != 200:
        flash("Erro ao obter o token de acesso.", "danger")
        return redirect(url_for("dashboard.meli_integracoes.index"))

    data_tokens = response.json()
    access_token = data_tokens.get("access_token")
    refresh_token = data_tokens.get("refresh_token")
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=data_tokens.get("expires_in", 3600)
    )
    user_id = data_tokens.get("user_id")

    # Verifica se já existe
    existing = MeliIntegracao.query.filter_by(
        user_id=current_user.id, meli_store_id=str(user_id)
    ).first()
    if existing:
        flash("Essa conta já está conectada.", "info")
        return redirect(url_for("dashboard.meli_integracoes.index"))

    integracao = MeliIntegracao(
        user_id=current_user.id,
        meli_nome=f"Conta Meli {user_id}",
        meli_store_id=str(user_id),
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )
    db.session.add(integracao)
    db.session.commit()

    meli_client = MeliClient(integracao)
    user_info = meli_client.post("users/me")
    
    integracao.meli_id = user_info.get("id", "")
    integracao.meli_nome = user_info.get("nickname", "")
    integracao.meli_email = user_info.get("email", "")
    integracao.meli_link = user_info.get("permalink", "")

    db.session.commit()

    flash("Conta Mercado Livre conectada com sucesso!", "success")
    return redirect(url_for("dashboard.meli_integracoes.index"))
