import pickle as pkl
import utils
import json
import os


hash_fn = utils.HashBytes(str).sha256


class Transaction(dict):
    # making it dict to insure json serializability.
    def __init__(self, data=''):
        if not any(map(lambda x: isinstance(x, data), (None, str))):
            raise ValueError('data should be either None or a string')
        self.data = data
        super().__init__(data=data)


class Block(object):
    def __init__(self, prev_hash, txs, difficulty_target, logger=None):
        self.difficulty_target = difficulty_target
        self.nonce = None
        self.merkle_root = None
        self.prev_hash = prev_hash
        self.logger = logger if logger is not None else utils.DefaultLogger()
        if not self.are_valid_txs(txs):
            raise ValueError('Transaction must be instances of {} class'.format(Transaction.__name__))
        self.txs = txs

    def are_valid_txs(self, txs):
        # allows empty collection of transactions
        return all(isinstance(tx, Transaction) for tx in txs)
 
    def generate_pow(self):
        self.nonce = 0
        while not self.valid_block():
            self.nonce += 1
        return self.nonce

    def mine_block(self):
        if self.valid_block():
            self.logger.log('Block was already mined.')
            return True
        self.logger.log('Mining this block. Generating it\'s pow')
        if not self.generate_pow():
            self.logger.log('Mining failed due to unknown reason.')
            return False
        self.logger.log('Mined the block successfully.')
        return True
    
    def valid_block(self):
        '''
        a block object is valid if it's hash matches the difficulty.
        '''
        return str(self.hash).startswith('0' * self.difficulty_target)

    @property
    def hash(self):
        self_params = self.__dict__.copy()
        self_params.pop('logger', None)
        data = json.dumps(self_params, sort_keys=True).encode()
        return hash_fn(data)
 
    def __repr__(self):
        return self.__dict__.__str__()


class Blockchain(object):
    def __init__(self, file_path, difficulty_target=4, load_from_file=False, logger=None, hash_fn=None):
        '''
        Args:
            difficulty_target <int>: number of 0's at the end of the block hashed with nonce.
            file_path <str>: Name of the file where blockchain will be saved.
            load_from_file <bool>: Load the blockchain stored in file_path
        '''
        self.file_path = file_path
        self.difficulty_target = difficulty_target
        self.load_from_file = load_from_file
        self.hash_fn = hash_fn if hash_fn is not None else utils.HashBytes().sha256
        self.current_transactions = []
        if logger is None:
            self.logger = utils.DefaultLogger()
        if self.load_from_file:
            self.chain = self.load_chain(file_path)
        else:
            self.chain = [Blockchain.create_genesis_block(self)]

    @staticmethod
    def create_genesis_block(self):
        init_tx = Transaction(data='Product Traceability using Blockchain by Rishabh, Sneha, Shrey')
        return Block('0', [init_tx], self.difficulty_target)

    def save_chain(self, file_path=None):
        file_path = file_path if file_path is not None else self.file_path
        if os.path.exists(file_path):
            choice = input('Do you want to write in the current file(y/*)? ')
            if not choice or choice not in 'Yy':
                self.logger.log('Current chain not written')
                return
            self.logger.log('Current chain was rewritten.')
        # chain should be written to the file
        with open(file_path, 'wb') as fh:
            # fh.write(pkl.dumps(self))
            pkl.dump(self, fh)

    def load_chain(self, file_path=None):
        file_path = file_path if file_path is not None else self.file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError("File named {} doesn't exists.".format(file_path))
        with open(file_path, 'rb') as fh:
            return pkl.load(fh)

    def create_block(self, txs):
        new_block = Block(self.chain[-1].hash, txs, self.difficulty_target)
        self.chain.append(new_block)

    def validate_chain(self):
        # checks if all the blocks are interlinked with their ancestors.
        # ll traversal:

        # note: it allows unmined genesis block.
        for curr, _next in zip(self.chain, self.chain[1:]):
            if not _next.valid_block() or _next.prev_hash != curr.hash:
                return False
        return True

