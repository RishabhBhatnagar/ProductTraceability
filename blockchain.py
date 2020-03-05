import pickle as pkl
import utils


class DefaultLogger:
    def __init__(self):
        pass
    def log(*args, **kw):
        print(*args, **kw)


class Transaction(object):
    def __init__(self, data=''):
        self.data = data


class Block(object):
    def __init__(self, prev_hash, txs, difficulty_target):
        self.diffulty_target = difficulty_target
        self.nonce = None
        self.merkle_root = None
        self.prev_hash = prev_hash
        if not self.are_valid_txs(txs):
            raise ValueError('Transaction must be instances of {} class'.format(Transaction.__name__))

    def are_valid_txs(self, txs):
        return all(isinstance(tx, Transaction) for tx in txs)



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
        self.hash_fn = hash_fn if hash_fn is not None else utils.HashBytes().sha256
        self.current_transactions = []
        if logger is None:
            self.logger = DefaultLogger()
        if self.load_from_file:
            self.chain = self.load_chain(file_path)

    def save_chain(self, file_path):
        file_path = file_path if file_path is not None else self.file_path
        if os.path.exists(file_path):
            choice = input('Do you want to write in the current file(y/*)')
            if choice not in 'Yy':
                self.logger.log('Current chain not written')
                return
        # chain should be written to the file
        pkl.dumps(self, file_path)

    def load_chain(self, file_path=None):
        file_path = file_path if file_path is not None else self.file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError("File named {} doesn't exists.".format(file_path))
        with open(file_path, 'rb') as fh:
            return pkl.load(fh)

    def hash(self, data):
        return self.hash_fn(data)
    def instantiate_blockchain(self):
        genesis_block = 

    def create_block(self, data):
        return Block(prev_hash = self.hash())

        
    hash
    pow
    mine_block
    validate_chain
    create_transaction
    
    load_chain
    serialise_chain
