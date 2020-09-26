import os
import re

import flask_restful as flask
import requests
from utils import DefaultLogger

STATIC_GITHUB_LINK = 'https://raw.githubusercontent.com/sem7vii/blockchain/master/link'
DATABASE_FILE_NAME = 'file'


def get_login_server_link():
    return re.sub('[\b\n\r\s]', '', requests.get(STATIC_GITHUB_LINK).text)


class ValidateUser(flask.Resource):
    def get(self, user_id, pswd_hash):
        global db
        return db.contains('{} {}'.format(user_id, pswd_hash))


class DataBase(object):
    def __init__(self, file_path, logger=None, force_write=False):
        '''
        file_path: path along with file name where user data will be stored.
        force_write: do you want to recreate a database with given file_path 
                     when a new object with same file_path is created.
        '''
        self.db_name = file_path
        self.force_write = force_write
        self.logger = DefaultLogger() if logger is None else logger
        self.instantiate_db()

    def instantiate_db(self):
        file_exists = os.path.exists(self.db_name)
        if file_exists:
            self.logger.log('{} already exists'.format(self.db_name))
        else:
            self.logger.log('{} doesn\'t exists'.format(self.db_name))
        if file_exists and not self.force_write:
            self.logger.log('not creating new')
            return
        with open(self.db_name, 'w'):
            pass
        self.logger.log('Created a new DB.')

    def add(self, rows):
        '''
        rows: list of lines to append to database.
             each line is a line joined using space.
        '''
        assert isinstance(rows, list)
        # appending \n to all the instances
        rows = [row + ('\n', '')[row.endswith('\n')] for row in rows]
        with open(self.db_name, 'a') as fh:
            fh.writelines(rows)

    def read(self):
        with open(self.db_name) as fh:
            return fh.read().split('\n')

    def contains(self, row):
        return row in '\n'.join(self.read())


'''
if __name__ == '__main__':
    db = DataBase('/media/pc-12/RishabhBhat/ProdTraceability/core/file')
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)
    api.add_resource(ValidateUser, '/validate_user/<string:user_id>/<string:pswd_hash>')
    app.run(host='192.168.31.32')
'''
