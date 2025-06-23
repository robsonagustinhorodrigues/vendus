import os
import requests
from datetime import datetime, timedelta, timezone
from models import db, MeliIntegration

class MeliClient:
    def __init__(self, meli_integracao):
        self.meli_integracao = meli_integracao 
    
    def get(self, endpoint, query_params=None, is_download=False):
        return self._request('GET', endpoint, query_params or {}, {}, is_download)

    def post(self, endpoint, data=None, is_download=False):
        return self._request('POST', endpoint, {}, data or {}, is_download)
    
    def _request(self, method, endpoint, query_params={}, data={}, is_download=False):

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
                raise Exception(f"Erro na API do Mercado Livre: {response.text}")

            if is_download:
                file_name = f"meli_{int(datetime.now().timestamp())}.zip"
                file_path = f"temp/{file_name}"
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return file_path

            return response.json()

        except Exception as e:
            print(f"Erro ao fazer requisição para o Mercado Livre: {str(e)}")
            raise
    
        
    def refresh_token(self):
            url = os.getenv('MELI_URL_TOKEN', 'https://api.mercadolibre.com/oauth/token')

            data = {
                'grant_type': 'refresh_token',
                'client_id': os.getenv('MELI_CLIENT_ID'),
                'client_secret': os.getenv('MELI_CLIENT_SECRET'),
                'refresh_token': self.meli_integracao.refresh_token
            }

            try:
                response = requests.post(url, data=data)
                if not response.ok:
                    raise Exception(f"Falha ao renovar token: {response.text}")

                token_data = response.json()

                self.meli_integracao.access_token = token_data.get('access_token', '')
                self.meli_integracao.refresh_token = token_data.get('refresh_token', '')
                self.meli_integracao.expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_data.get('expires_in', 3600))
                self.meli_integracao.meli_user_id = str(token_data.get('user_id', ''))

                from models import db
                db.session.commit()

            except Exception as e:
                print(f"Erro ao renovar token: {str(e)}")
                raise

    def token_expirado(self):
        return datetime.now(timezone.utc) >= self.meli_integracao.expires_at