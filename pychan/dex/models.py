import requests

from django.db import models

# Create your models here.
class Wallet(models.Model):

    def get_balance(public_address):
        data = {
            'public_address': public_address
        }
        req = requests.get('http://localhost:5000/dex/balance', json=data)

