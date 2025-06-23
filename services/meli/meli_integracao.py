import os
import requests
from datetime import datetime, timedelta, timezone
from models import db, MeliIntegracao
from services.meli.client_meli import MeliClient

class MeliIntegracao:
    def __init__(self, meli_integracao):
        self.meli_integracao = meli_integracao
        
    def get_me():
        endpoint = "/users/me"
        meli_client = MeliClient(self.meli_integracao)
        user_info = meli_client.post(endpoint)
    
        return user_info