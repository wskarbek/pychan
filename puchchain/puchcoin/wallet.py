from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import Crypto.Random
import binascii


class Wallet:
    def __init__(self, node_id):
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    @staticmethod
    def generate_keys():
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.public_key()
        return binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(
            public_key.exportKey(format='DER')).decode('ascii')

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key is not None and self.private_key is not None:
            try:
                with open('wallet-{}.dat'.format(self.node_id), mode='w') as f:
                    f.write(self.public_key)
                    f.write("\n")
                    f.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('Saving wallet failed...')
                return False

    def load_keys(self):
        try:
            with open('wallet-{}.dat'.format(self.node_id), mode='r') as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
            return True
        except (IOError, IndexError):
            print('Loading wallet failed...')
            return False


    @staticmethod
    def sign_tx_with_pkey(private_key, sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    def sign_tx(self, sender, recipient, amount):
        return Wallet.sign_tx_with_pkey(self.private_key, sender, recipient, amount)


    @staticmethod
    def verify_tx(tx):
        public_key = RSA.importKey(binascii.unhexlify(tx.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(tx.sender) + str(tx.recipient) + str(tx.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(tx.signature))

    def sign_post(self, board, thread, image, timestamp, message):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((board + str(thread) + str(image) + str(timestamp) + str(message)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_post(post):
        return True
        public_key = RSA.importKey(binascii.unhexlify(post.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((post.board + str(post.thread) + str(post.image) + str(post.timestamp) + str(post.message)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(post.signature))