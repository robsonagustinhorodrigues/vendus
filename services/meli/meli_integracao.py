import os
import requests
from datetime import datetime, timedelta, timezone
from models import db, MeliIntegracao
from services.meli.meli_client import MeliClient

class MeliIntegracao:
    def __init__(self, meli_integracao):
        self.meli_integracao = meli_integracao
    
        
    def get_me(self):
        user_info = {}
        try:
            endpoint = "/users/me"
            
            meli_client = MeliClient(self.meli_integracao)

            if self.meli_integracao.token_expirado():
                meli_client.refresh_token()

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
            
    def update_integracao(self):
        try:
            user_info = self.get_me()
            if user_info['status'] == 'success':
                data = user_info['data']
                self.meli_integracao.meli_nome = data.get('nickname', self.meli_integracao.meli_nome)
                self.meli_integracao.meli_email = data.get('email', self.meli_integracao.meli_email)
                self.meli_integracao.meli_link = data.get('permalink', self.meli_integracao.meli_link)
                self.meli_integracao.meli_id = data.get('id', self.meli_integracao.meli_id)
                
                db.session.commit()
                return True
            else:
                raise Exception(user_info['message'])
        except Exception as e:
            raise e
        
        
    def get_analisar_reputacao(self):
        meli_id = self.meli_integracao.meli_store_id
        meli = MeliClient(self.meli_integracao)
        
        user_me = meli.get("/users/me")
        # user_data = meli.get(f"/users/{meli_id}")
        seller_recovery = meli.get("/users/reputation/seller_recovery/status")
        # users_cap = meli.get("/marketplace/users/cap")
        # user_metrics = meli.get(f"/users/{meli_id}/metrics")
        # users_shipping_preferences = meli.get("/users/{meli_id}/shipping_preferences")
        
        
        return {
            "meli_id": meli_id,
            "user_me" : user_me,
            # "user_data": user_data,
            "seller_recovery": seller_recovery,
            # "users_cap": users_cap,
            # "user_metrics": user_metrics,
            # "users_shipping_preferences": users_shipping_preferences
        }
