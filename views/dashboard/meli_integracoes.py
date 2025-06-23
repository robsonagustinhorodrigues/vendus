from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, MeliIntegracao

meli_integracoes = Blueprint('meli_integracoes', __name__)

@meli_integracoes.route('/')
@login_required
def index():
    meli_integracoes = MeliIntegracao.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/meli_integracoes.html', meli_integracoes=meli_integracoes)

@meli_integracoes.route('/adicionar', methods=['POST'])
@login_required
def adicionar():    
    meli_nome = request.form.get('nome')
    meli_store_id = request.form.get('store_id')

    if meli_nome and meli_store_id:
        meli_store_id = str(meli_store_id)
        nova = MeliIntegracao(
            meli_nome=meli_nome,
            meli_store_id=meli_store_id,
            user_id=current_user.id,
            access_token='TEMPORARIO',  # depois substitua com a autenticação real
        )
        db.session.add(nova)
        db.session.commit()
        flash('Integração adicionada com sucesso!', 'success')
    else:
        flash('Preencha todos os campos.', 'danger')

    return redirect(url_for('meli_integracoes.index'))

@meli_integracoes.route('/remover', methods=['POST'])
@login_required
def remover():
    integracao_id = request.form.get('id')
    integracao = MeliIntegracao.query.get(integracao_id)

    if integracao and integracao.user_id == current_user.id:
        db.session.delete(integracao)
        db.session.commit()
        flash('Integração removida com sucesso!', 'success')
    else:
        flash('Erro ao remover integração.', 'danger')

    return redirect(url_for('meli_integracoes.index'))
