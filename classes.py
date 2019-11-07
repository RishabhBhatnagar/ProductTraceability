class Node(object):
    def __init__(self, prev_hash):
        self.prev_hash = prev_hash
        self.merkle_root = None
        self.nonce = None
        self.difficulty_target = 4
        self.list_transactions = []

