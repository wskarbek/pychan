import binascii
import json

from flask import Flask, jsonify, request as req
from Crypto.PublicKey import RSA

from puchcoin.blockchain import Blockchain
from puchcoin.wallet import Wallet

NODE = "TESTNET"

app = Flask(__name__)

wallet = Wallet(NODE)
blockchain = None

if(wallet.load_keys() == False):
    print("Creating new wallet...")
    wallet.create_keys()
    wallet.save_keys()
blockchain = Blockchain(wallet.public_key, NODE)

@app.route('/dex', methods=['GET'])
@app.route('/dex/balance', methods=['GET'])
def get_balance():
    return str(blockchain.get_balance(req.json['public_address']))

@app.route('/dex/create', methods=['GET'])
def create_wallet():
    private_key, public_key = Wallet.generate_keys()
    return {
        'private_key': private_key,
        'public_key': public_key
    }

@app.route('/dex/send', methods=['POST'])
def add_transaction():
    tx_kwargs = req.json
    tx_kwargs['amount'] = int(tx_kwargs['amount'])
    tx_kwargs['private_key'] = tx_kwargs['private_key'].encode('utf-8')
    tx_kwargs['signature'] = Wallet.sign_tx_with_pkey(**tx_kwargs)
    blockchain.add_transaction(**tx_kwargs)
    return "Success"

@app.route('/post/', methods=['POST'])
def add_post():
    signature = wallet.sign_post(
        'test',
        req.json['thread'],
        'test',
        req.json['timestamp'],
        req.json['message'],
    )
    blockchain.add_post(
        'test',
        req.json['thread'],
        'test',
        req.json['timestamp'],
        req.json['message'],
        signature
    )
    return "cope"

@app.route('/chain/mine', methods=['POST'])
def mine_block():
    blockchain.mine_block()
    return "Mined"
    