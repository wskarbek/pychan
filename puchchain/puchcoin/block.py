from time import time
import json
import hashlib

class Block:
    def __init__(self, index, previous_hash, txs, posts, proof, timestamp=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.txs = txs
        self.posts = posts
        self.proof = proof

    def __repr__(self):
        return 'BLOCK: {}, HASH: {}, PROOF: {}, TXS: {}, POSTS: {}'\
            .format(self.index, self.previous_hash, self.proof, self.txs, self.posts)

    @staticmethod
    def hash_string(string):
        return hashlib.sha256(string).hexdigest()

    @staticmethod
    def hash_block(block):
        """Hashes a block and returns the hash.
        Arguments:
            :block: The block that will be hashed.
        """
        hashable_block = block.__dict__.copy()
        hashable_block['txs'] = [tx.to_ordered_dict() for tx in hashable_block['txs']]
        return Block.hash_string(json.dumps(hashable_block, sort_keys=True).encode())
