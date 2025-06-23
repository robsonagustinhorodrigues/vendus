import os
import requests
import logging
from datetime import datetime, timedelta, timezone
from models import db, MeliIntegracao

logger = logging.getLogger(__name__)

class MeliClient:
    def __init__(self, meli_integracao):
        self.meli_integracao = meli_integracao 
    
    def get(self, endpoint, query_params=None, is_download=False):
        return self._request('GET', endpoint, query_params or {}, {}, is_download)

    def post(self, endpoint, data=None, is_download=False):
        return self._request('POST', endpoint, {}, data or {}, is_download)
    
    def _request(self, method, endpoint, query_params={}, data={}, is_download=False):

        # Verifica se o token expirou e renova se necessário
        if self.token_expirado():
            self.refresh_token()

        base_url = os.getenv('MELI_URL_API', 'https://api.mercadolibre.com')
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        headers = {
            'Authorization': f"Bearer {self.meli_integracao.access_token}"
        }

        try:
            if method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=query_params)
            else:
                response = requests.request(method, url, headers=headers, json=data)

            if not response.ok:
                try:
                    error_msg = response.json().get('message', response.text)
                except Exception:
                    error_msg = response.text
                raise Exception(f"Erro na API do Mercado Livre: {error_msg}")

            if is_download:
                file_name = f"meli_{int(datetime.now().timestamp())}.zip"
                file_path = f"temp/{file_name}"
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return file_path

            return response.json()

        except Exception as e:
            logger.error(f"Erro ao fazer requisição para o Mercado Livre: {str(e)}")
            raise

    def refresh_token(self):
        url = os.getenv('MELI_URL_TOKEN', 'https://api.mercadolibre.com/oauth/token')

        client_id = os.getenv('MELI_CLIENT_ID')
        client_secret = os.getenv('MELI_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise Exception("Variáveis de ambiente MELI_CLIENT_ID ou MELI_CLIENT_SECRET não definidas")

        data = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': self.meli_integracao.refresh_token
        }

        try:
            response = requests.post(url, data=data)
            if not response.ok:
                try:
                    error = response.json().get("message", response.text)
                except:
                    error = response.text
                raise Exception(f"Falha ao renovar token: {error}")

            token_data = response.json()

            self.meli_integracao.access_token = token_data.get('access_token', '')
            self.meli_integracao.refresh_token = token_data.get('refresh_token', '')
            self.meli_integracao.expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_data.get('expires_in', 3600))
            self.meli_integracao.meli_user_id = str(token_data.get('user_id', ''))

            db.session.commit()

        except Exception as e:
            logger.error(f"Erro ao renovar token: {str(e)}")
            raise

    def token_expirado(self):
        now = datetime.now(timezone.utc)
        expires_at = self.meli_integracao.expires_at

        # Garante que ambos sejam datetime com timezone (offset-aware)
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        return now >= expires_at
