"""
Module That will provide all the required classes for the project.
"""

import _sha256
import _sha512


class HashBytes(object):
    """Hashing ByteLike objects"""
    def __init__(self, return_type=str):
        """
        Class to bind all the methods associated with Hashing Bytes together
        Args:
            return_type: can be either str or bytes.
        Raises:
            TypeError: if return_type is not str or bytes.
        """
        if return_type not in (bytes, str):
            raise TypeError("Expected either bytes or str")
        self.return_type = return_type

    @classmethod
    def check_bytes(cls, func):
        """
            Decorator which checks if the input to the hash function is bytes.
            Args:
                func: A callable hash function accepting bytes as input.
            Returns:
                Wrapper which checks for correctness and evaluate the results.
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
            except:
                raise TypeError("Expected a Byte Like Object")
        return inner

    def adj_return_type(self, hash_bytes):
        """
        Adjusts the return type according the demand of user.
        Args:
            hash_bytes: byte like object.
        Returns:
            byte or str representation of the input as defined in the instance.
        """
        if self.return_type == str:
            return hash_bytes.hexdigest()
        else:
            return hash_bytes

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

    @classmethod
    def convert_to_bytes(cls, ip_str):
        """
        Convert the input string to bytes.
        Args:
            ip_str: string to be converted to bytes
        """
        try:  # EAFP
            return str.encode(ip_str)
        except:
            raise ValueError("String expected. Found {}".format(type(ip_str)))

    sha256 = lambda self, ip_str: super().sha256(self.convert_to_bytes(ip_str))
    sha512 = lambda self, ip_str: super().sh512(self.convert_to_bytes(ip_str))


class Node(object):
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
        pass

    def validate_chain(self):
        """Not Implemented Yet"""
        pass

    def get_acc_info(self):
        """Not Implemented Yet"""
        pass

