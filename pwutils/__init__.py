from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac
from os import urandom
from sqlescapy import sqlescape
from flask import escape

INVPWMSG = "Inputted password was invalid"


def hash_pw(password):
    salt = urandom(256)
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hashedpw = hexlify(salt + key)
    return hashedpw.decode('utf-8')


def compare_pw(pwhashin, password):
    salt = unhexlify(pwhashin.encode('utf-8'))[:256]
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    pwhashcomputed = hexlify(salt + key)
    decoded = pwhashcomputed.decode('utf-8')
    return bool(pwhashin == decoded)


def validate_password(password):
    password = str(password)
    if len(password) < 8:
        raise ValueError(INVPWMSG)
    with open('10-million-password-list-top-500.txt', 'r') as badpwlist:
        rejectpwlist = str(badpwlist.read()).split('\n')
        if password in rejectpwlist:
            raise ValueError(INVPWMSG)
    return password


def validate_username(username):
    username = list(str(username))
    username[0] = username[0].upper()
    username = str(''.join(username))
    return escape(sqlescape(str(username).replace(' ', '_')))
