"""
All the functions related to ipfs are present in this file.
"""


import os
import re
import sys
import math
import subprocess
import utils


IPFS_LINKS = {
    32: dict(
        nt='https://dist.ipfs.io/fs-repo-migrations/v1.4.0/'
           'fs-repo-migrations_v1.4.0_windows-386.zip',
        posix='https://dist.ipfs.io/go-ipfs/v0.4.23/'
              'go-ipfs_v0.4.23_linux-386.tar.gz'
    ),
    64: dict(
        nt='https://dist.ipfs.io/fs-repo-migrations/v1.4.0/'
           'fs-repo-migrations_v1.4.0_windows-amd64.zip',
        posix='https://dist.ipfs.io/go-ipfs/v0.4.23/'
              'go-ipfs_v0.4.23_linux-amd64.tar.gz'
    )
}
COMMAND_NOT_FOUND_ERROR = 32512


def ipfs_installed():
    '''
    Checks if ipfs is already installed in this machine.
    '''
    if os.system('ipfs --version') != COMMAND_NOT_FOUND_ERROR:
        return True
    return False


def install_ipfs(quiet=False):
    '''
    Installs the ipfs software for windows and linux systems.
    '''
    if ipfs_installed():
        return True
    os_name = os.name   # either of ('posix', 'nt', 'java')
    n_bits = 32 << bool(sys.maxsize >> 32)
    ipfs_url = IPFS_LINKS.get(n_bits, dict()).get(os_name, None)
    file_extension = ('zip', 'tar.gz')[os.name == 'posix']
    output_file_name = 'ipfs.' + file_extension
    ipfs_dir_name = 'go-ipfs'     # dir after unzipping.
    if ipfs_url is None:
        raise NotImplementedError('Program doesn\'t support your OS yet.')
    downloaded = utils.wget(
        ipfs_url,
        output_document=output_file_name,
        tries=math.inf,
        timeout=100,
        quiet=quiet
    )
    if downloaded:
        utils.unzip(output_file_name)
        os.chdir(ipfs_dir_name)
        if os_name == 'posix':
            os.system('sudo ./install.sh')
        else:
            os.system('ipfs')
        os.chdir('..')
        if not quiet:
            print('IPFS installed successfully.')
            print('Removing intermediate files...')
        os.remove(output_file_name)
        return True
    return False


def upload_from_path(path):
    '''
    Upload all the files in the path
    OR
    Upload the file if path is a file.
    Args:
        file <str>: path to the file/directory
    Returns: 
        hash_value <NoneType/str>: hash of the uploaded file
    '''
    # check if path exists and is valid.
    if not os.path.exists(path):
        raise ValueError("{}: No such file or directory.".format(path))
    if not ipfs_installed():
        print('Installing IPFS....')
        install_ipfs()
    utils.run_command('ipfs init')
    ADD_COMMAND = 'ipfs add ' + '-r ' * os.path.isdir(path) + path
    op = utils.run_command(ADD_COMMAND)
    # op is in the form "added hash filename"

    try:
        hash_values = re.findall('(?<=added\s)\w+', op)
    except:
        return None   # File couldn't be uploaded
    for hash_value in hash_values:
        utils.run_command('ipfs pin add ' + hash_value)
    return hash_values


