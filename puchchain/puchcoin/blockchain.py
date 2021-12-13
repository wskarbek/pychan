import json
#import requests

from puchcoin.block import Block
from puchcoin.transaction import Transaction
from puchcoin.post import Post
from puchcoin.wallet import Wallet
from puchcoin.verifier import Verification

MINING_REWARD = 1000


class Blockchain:
    def __init__(self, user, node_id):
        self.genesis_block = Block(0, 'GENESIS', [], 100, 0)
        self.verifier = Verification()
        self.chain = [self.genesis_block]
        self.__open_transactions = []
        self.__open_posts = []
        self.__peer_nodes = set()
        self.stakers = set()
        self.user = user
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_txs(self):
        return self.__open_transactions

    def save_data(self):
        try:
            with open('puch-{}.blockchain'.format(self.node_id), mode='w') as f:
                f.write(json.dumps([block.__dict__ for block in [
                    Block(block_el.index,
                          block_el.previous_hash,
                          [tx.__dict__ for tx in block_el.txs],
                          block_el.proof,
                          block_el.timestamp
                          ) for block_el in self.chain]]))
                f.write('\n')
                f.write(json.dumps([tx.__dict__ for tx in self.__open_transactions]))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': __open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')

    def load_data(self):
        try:
            with open('puch-{}.blockchain'.format(self.node_id), mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()

                # blockchain = file_content['chain']
                # __open_transactions = file_content['ot']
                self.chain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in self.chain:
                    converted_txs = [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['signature'],
                        tx['amount']
                    ) for tx in block['txs']]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_txs,
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                __open_transactions = json.loads(file_content[1][:-1])
                updated_open_txs = []
                for tx in __open_transactions:
                    updated_open_tx = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_open_txs.append(updated_open_tx)
                self.__open_transactions = updated_open_txs
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except IOError:
            self.chain = [self.genesis_block]
            self.__open_transactions = []

    def get_balance(self, sender):
        """Gets balance of a user and returns it as float. Total balance is reduced staked transactions, but finished stakes are ignored.

        Keyword Args:
            sender -- public key of a user we want to get balance for
        """
        if sender is None:
            if self.user is None:
                return None
            participant = self.user
        else:
            participant = sender
        tx_sender = [[tx.amount for tx in block.txs if tx.sender == participant] for block in self.chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = 0
        for tx in tx_sender:
            if len(tx) > 0:
                amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.txs if tx.recipient == participant] for block in
                        self.chain]
        amount_received = 0
        for tx in tx_recipient:
            if len(tx) > 0:
                amount_received += tx[0]
        return amount_received - amount_sent

    def add_transaction(self, sender, recipient, signature, amount, is_receiving=False, **kwargs):
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_tx(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            #if not is_receiving:
            #    for node in self.__peer_nodes:
            #        url = 'http://{}/broadcast-transaction'.format(node)
            #        tx_json = {
            #            'sender': sender,
            #            'recipient': recipient,
            #            'amount': amount,
            #            'signature': signature
            #        }
            #        try:
            #            res = requests.post(url, json=tx_json)
            #            if res.status_code == 400 or res.status_code == 500:
            #                print('TX failed.')
            #                return False
            #        except requests.exceptions.ConnectionError:
            #            continue
            return True
        return False

    def add_post(self, board, thread, image, timestamp, message, signature):
        post = Post(None, thread, None, timestamp, message, signature)
        self.__open_posts.append(post)
        self.save_data()


    def add_block(self, block):
        transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['txs']]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = Block.hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['txs']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.signature == itx['signature'] and opentx.amount == itx['amount']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed')
        self.save_data()
        return True

    #def resolve(self):
    #    winner_chain = self.chain
    #    replace = False
    #    for node in self.__peer_nodes:
    #        url = 'http://{}/chain'.format(node)
    #        try:
    #            res = requests.get(url)
    #            node_chain = res.json()
    #            node_chain = [Block(block['index'], block['previous_hash'], [Transaction(
    #                tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']],
    #                                block['proof'], block['timestamp']) for block in node_chain]
    #            node_chain_length = len(node_chain)
    #            local_chain_length = len(winner_chain)
    #            if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
    #                winner_chain = node_chain
    #                replace = True
    #        except requests.exceptions.ConnectionError:
    #            continue
    #    self.resolve_conflicts = False
    #    self.chain = winner_chain
    #    if replace:
    #        self.__open_transactions = []
    #    self.save_data()
    #    return replace

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = Block.hash_block(last_block)
        proof = 0
        while not self.verifier.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def mine_block(self):
        if self.user is None:
            return None
        last_block = self.chain[-1]
        hashed_block = Block.hash_block(last_block)
        proof = self.proof_of_work()
        print(self.__open_transactions)
        reward_transaction = Transaction('GENESIS', self.user, '', MINING_REWARD)
        # Verify txs
        open_tx_copy = self.__open_transactions[:]
        for tx in self.__open_transactions:
            if not Wallet.verify_tx(tx):
                return False
        open_tx_copy.append(reward_transaction)
        # Verify posts
        open_posts_copy = self.__open_posts
        for post in self.__open_posts:
            if not Wallet.verify_post(post):
                return False
        block = Block(
            len(self.chain),
            hashed_block,
            open_tx_copy,
            open_posts_copy,
            proof
        )
        print(block)
        print('-' * 197)
        self.__chain.append(block)
        self.__open_transactions.clear()
        self.save_data()
        #for node in self.__peer_nodes:
        #    url = 'http://{}/broadcast-block'.format(node)
        #    converted_block = block.__dict__.copy()
        #    converted_block['txs'] = [tx.__dict__ for tx in converted_block['txs']]
        #    try:
        #        res = requests.post(url, json={'block': converted_block})
        #        if res.status_code == 400 or res.status_code == 500:
        #            print('Block declined')
        #        if res.status_code == 409:
        #            self.resolve_conflicts = True
        #    except requests.exceptions.ConnectionError:
        #        continue
        return block