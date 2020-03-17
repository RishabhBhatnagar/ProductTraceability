import uuid
import utils
import unittest
import unittest.mock as mock


class TestHashBytes(unittest.TestCase):
    def test(self):
        # input_type: byte, return_type:str
        hasher = utils.HashBytes()
        h1 = hasher.sha512(b'abc')
        h2 = hasher.sha256(b'abc')
        self.assertIsInstance(h1, str)
        self.assertIsInstance(h2, str)
        self.assertIsInstance(utils.HashBytes(bytes).sha256(b'abc'), bytes)
        self.assertRaises(TypeError, lambda: hasher.sha512('abc'))
        self.assertRaises(TypeError, lambda: hasher.sha512(self))


class TestHashStrings(unittest.TestCase):
    def test(self):
        # input_type: byte, return_type: bytes
        hasher = utils.HashStrings()
        h1 = hasher.sha512('abc')
        self.assertIsInstance(h1, str)
        self.assertIsInstance(utils.HashStrings(bytes).sha512('abc'), bytes)
        self.assertRaises(TypeError, lambda: hasher.sha512(b'asdf'))
        self.assertRaises(TypeError, lambda: hasher.sha512(123))


class TestHashFiles(unittest.TestCase):
    '''
    create: create attributes that doesn't exists.
    first_parameter: function to be mocked.
    '''
    def test_file_absent(self):
        file_name = str(uuid.uuid4())
        hasher = utils.HashFiles()
        self.assertRaises(FileNotFoundError, lambda: hasher.sha512(file_name))

    @mock.patch('os.path.exists', lambda x: True)
    @mock.patch('builtins.open', mock.mock_open(read_data=b''))
    def test_file_present_with_permission(self):
        hasher = utils.HashFiles()
        self.assertIsInstance(hasher.sha256('file'), str)

