"""
Module That will provide all the required classes for the project.
"""

import os
import sys
import hashlib
import urllib
import urllib.parse
import urllib.error
import urllib.request
import builtins
import tarfile
import zipfile
import subprocess


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

    def check_bytes(self, data):
        if isinstance(data, bytes):
            return True
        raise TypeError('Data must be of type <bytes>.')

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

    def sha256(self, data):
        """ sha256 """
        self.check_bytes(data)
        return self.adj_return_type(hashlib.sha256(data))

    def sha512(self, data):
        """ sha512 """
        self.check_bytes(data)
        return self.adj_return_type(hashlib.sha512(data))


class HashStrings(HashBytes):
    """
    Given a String, Hash it.
    """
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


def read_file_bin(file_addr):
    '''
    Read the file from the given path.
    Args:
        file_path <str>: address of the file where it is stored.
    Returns:
        Content of the file in byte format.
    Raises
        FileNotFoundError: when file_addr doesn't exist.
        PermissionError:   when file is not readable.
                           # sudo chmod +r file_addr
    '''
    if not os.path.exists(file_addr):
        raise FileNotFoundError(
            'File Named <{}> doesn\'t exists'.format(file_addr)
        )
    content = None
    with open(file_addr, 'rb') as file_handler:
        content = file_handler.read()
    return content


class HashFiles(HashBytes):
    '''Hash the contents of a file given file_path'''
    def sha512(self, file_addr):
        return super().sha512(read_file_bin(file_addr))

    def sha256(self, file_addr):
        return super().sha256(read_file_bin(file_addr))


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


def wget(url, output_document=None, input_file=None, tries=20, quiet=False, timeout=900):
    '''
    wget equivalent in python3 made especially for windows' users.
    Args:
        url              <string>    : url of the file on the internet
        output_document  <string>    : file_name where fetched file should .
                                       be stored.
        input_file       <string>    : the file path from where input links
                                       should be read.
        tries            <int/float> : in case of timeouts, how many times
                                       should wget retry fetching the file.
                                       can be any integer or math.inf
        quiet            <bool>      : Does user want any output on the stdout.
        timeout          <int>       : should be a natural number
    Returns:
        successful <bool> : If fetching all the files was successful.
    '''
    log = lambda *x, **xx: None if quiet else builtins.print(*x, *xx)

    if timeout <= 0:
        raise ValueError("Timeout should be greater than 0.")

    if input_file is not None:
        # read links from the mentioned file path.
        try:
            with open(input_file, 'r') as file_handler:
                links = file_handler.read().split('\n')

            # stripping all redundant newlines and white spaces.
            links = [l for l in map(lambda l: l.strip(), links) if l]
        except FileNotFoundError:
            raise FileNotFoundError('File {} not found.'.format(input_file))
        except PermissionError:
            raise PermissionError('File {} not readable.'.format(input_file))

        if len(links) > 1 and output_document is not None:
            # found multiple files to be downloaded but
            #     only one output file name.
            raise ValueError('Don\'t know which file to be stored where.')

        # fetch all the files stored in links recursively(one level deep).
        for link in links:
            log('Found more than one links in the file.')
            log('Downloading it in FCFS order.')
            return all(wget(link, tries))

    try:
        # parse url to check if it's valid (EAFP).
        parsed_url = urllib.parse.urlparse(url)
    except ValueError:
        raise ValueError("Invalid URL: {}".format(url))

    if output_document is None:
        output_document = os.path.basename(parsed_url.path)
    log('Storing the File in', output_document)

    epoch = 0
    while epoch < tries:
        epoch += 1
        try:
            log('Trying {}th time'.format(epoch))
            response = urllib.request.urlopen(url, timeout=timeout)
            with open(output_document, 'wb') as file_handler:
                file_handler.write(response.read())
            log("File from {} Downloaded Successfully....".format(url))
            return True  # successfully downloaded the file.
        except urllib.error.URLError as err:
            log(type(err))
    return False


def unzip(file_path):
    '''
    Unzips tar.gz or zip files in current folder.
    Args:
        file_path <str>: path to the zip file alongwith filename.
    '''
    if file_path.endswith('gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall()
    elif file_path.endswith('zip'):
        with zipfile.ZipFile(file_path, 'r') as zfh:
            zfh.extractall('.')


def run_command(command):
    '''
    Runs the given command and returns the output ignoring any stderr.
    Args:
        command <str>: command to execute on shell.
    Returns:
        op <str>: output of the execution.
    '''
    print("running this command:", command)
    op = subprocess.run(command.split(), stdout=subprocess.PIPE).stdout
    return op.decode('utf8')


class DefaultLogger:
    def __init__(self):
        pass
    def log(self, *args, **kw):
        # Augiwan's answer: https://stackoverflow.com/questions/2654113/how-to-get-the-callers-method-name-in-the-called-method
        caller = sys._getframe().f_back.f_code.co_name
        print('{} says: :'.format(caller), *args, **kw)
