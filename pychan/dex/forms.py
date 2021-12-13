import binascii
import requests

from Crypto.PublicKey import RSA

from django import forms

class CreateWalletForm(forms.Form):

    def get_keys(self):
        return requests.get('http://localhost:5000/dex/create').json()


class SendForm(forms.Form):
    private_key = forms.CharField(label='Private key')
    public_key = forms.CharField(label='Public key')
    recipient = forms.CharField(label='Recipient')
    amount = forms.DecimalField(label='Amount')
    
    def send_crypto(self, private_key, public_key, recipient, amount, **kwargs):
        data = {
            'private_key': private_key[0],
            'sender': public_key[0],
            'recipient': recipient[0],
            'amount': amount[0]
        }
        return requests.post('http://localhost:5000/dex/send', json=data).json
