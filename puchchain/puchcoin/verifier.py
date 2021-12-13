from puchcoin.block import Block 
from puchcoin.wallet import Wallet

class Verification:
    @staticmethod
    def verify_tx(transaction, get_balance, check_funds=True):
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_tx(transaction)
        else:
            return Wallet.verify_tx(transaction)

    @classmethod
    def verify_txs(cls, open_txs, get_balance):
        return all([cls.verify_tx(tx, get_balance, False) for tx in open_txs])

    @staticmethod
    def valid_proof(txs, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in txs]) + str(last_hash) + str(proof)).encode()
        guess_hash = Block.hash_string(guess)
        # print(guess_hash)
        return guess_hash[0:2] == 'ff'

    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != Block.hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.txs[:-1], block.previous_hash, block.proof):
                print('PoW is invalid')
                return False
        return True