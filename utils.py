"""
Module That will provide all the required classes for the project.
"""

import _sha256
import _sha512


def check_bytes(func):
    """
        Decorator which checks if the input to the hash function is bytes.
        Args:
            func <Callable>: A hash function accepting bytes as input.
        Returns:
            <Callable>: Wrapper which checks for correctness and evaluate the results.
    """
    def inner(_input, *args, **kwargs):
        """
        Actual wrapper which will check if the input is bytes.
        Args:
            _input: bytes input
        Raises:
            TypeError: if the _input is not bytes.
        """
        try:
            return func(_input, *args, **kwargs)
        except TypeError:
            raise TypeError("Expected a Byte Like Object")
    return inner


class HashBytes:
    """Hashing ByteLike objects"""
    def __init__(self, return_type=str):
        """
        Class to bind all the methods associated with Hashing Bytes together
        Args:
            return_type <type>: can be either str or bytes.
        Raises:
            TypeError: if return_type is not str or bytes.
        """
        if return_type not in (bytes, str):
            raise TypeError("Expected either bytes or str")
        self.return_type = return_type


    def adj_return_type(self, hash_bytes):
        """
        Adjusts the return type according the demand of user.
        Args:
            hash_bytes <bytes>: byte like object.
        Returns:
            <byte/str>: result according to self.return_type
        """
        if self.return_type == str:
            return hash_bytes.hexdigest()
        return hash_bytes.digest()

    @check_bytes
    def sha256(self, data):
        """ sha256 """
        return self.adj_return_type(_sha256.sha256(data))

    @check_bytes
    def sha512(self, data):
        """ sha512 """
        return self.adj_return_type(_sha512.sha512(data))


class HashStrings(HashBytes):
    """
    Given a String, Hash it.
    """
    def __init__(self, return_type=str):
        super().__init__()
    @classmethod
    def convert_to_bytes(cls, ip_str):
        """
        Convert the input string to bytes.
        Args:
            ip_str <str>: string to be converted to bytes
        Returns:
            <bytes>: byte representation of the ip_str.
        """
        try:  # EAFP
            return str.encode(ip_str)
        except ValueError:
            raise ValueError("String expected. Found {}".format(type(ip_str)))

    def sha256(self, data):
        return super().sha256(self.convert_to_bytes(data))
    def sha512(self, data):
        return super().sha512(self.convert_to_bytes(data))


class Node:
    """
    Basic Blockchain Node.
    """
    def __init__(self, prev_hash):
        """
        Some of the many attributes has been added.
        """
        self.prev_hash = prev_hash
        self.merkle_root = None
        self.nonce = None
        self.difficulty_target = 4
        self.list_transactions = []

    def mine(self):
        """Abstract method yet to be implemented"""

    def validate_chain(self):
        """Not Implemented Yet"""

    def get_acc_info(self):
        """Not Implemented Yet"""

