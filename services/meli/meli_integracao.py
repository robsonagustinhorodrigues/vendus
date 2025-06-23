import os
import requests
from datetime import datetime, timedelta, timezone
from models import db, MeliIntegracao
from services.meli.client_meli import MeliClient

class MeliIntegracao:
    def __init__(self, meli_integracao):
        self.meli_integracao = meli_integracao
    
        
    def get_me(self):
        user_info = {}
        try:
            endpoint = "/users/me"

            if self.meli_integracao.token_expirado():
                self.meli_integracao.renovar_token()
                db.session.commit()

            meli_client = MeliClient(self.meli_integracao)

            user_info = meli_client.get(endpoint)
            
            return {
                "status": "success",
                "data": user_info,
                "raw": user_info
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "raw": user_info
            }
