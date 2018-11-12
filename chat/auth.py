import os
import hashlib


def check_password(password, pass_hash, pass_salt):
    '''
    Check given password if it corresponds to the pass_hash and pass_salt
    that are meant to be stored in the DB.
    '''
    return hashlib.sha256(pass_salt + password).hexdigest() == pass_hash


def gen_hash(password):
    '''
    Generates a dict with hash and salt.
    Hash and salt values can be stored directly in text fields of the DB,
    as they contain hex characters only.
    '''
    output = dict()
    output['salt'] = os.urandom(32).encode('hex')
    output['hash'] = hashlib.sha256(output['salt'] + password).hexdigest()
    return output
