#!/usr/bin/env python
# encoding: utf-8

"""
@time: 17-2-10 下午7:41
@author: Darkmelody(xx@nop.pw)
@version: 1.0.0
"""

import hashlib
from Crypto.Cipher import AES
import base64
import array
from urllib import unquote
import json, sys


class AesCrypter(object):
    def __init__(self, key, iv):
        self.key = hashlib.sha256(key).digest()
        self.iv = array.array('B', iv.decode('hex')).tostring()

    def encrypt(self, data):
        data = unquote(base64.b64decode(data))
        data = self.pkcs7padding(data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(data)
        return base64.b64encode(encrypted)

    def decrypt(self, data):
        data = unquote(data)
        data = base64.b64decode(data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(data)
        decrypted = self.pkcs7unpadding(decrypted)
        return decrypted

    def pkcs7padding(self, data):
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = chr(padding) * padding
        return data + padding_text

    def pkcs7unpadding(self, data):
        lengt = len(data)
        unpadding = ord(data[lengt - 1])
        return data[0:lengt - unpadding]


if __name__ == '__main__':
    key = base64.b64decode(sys.argv[1])
    iv = sys.argv[2]
    crypttype = sys.argv[3]
    hashstr = sys.argv[4]
    aes = AesCrypter(key, iv)
    if crypttype == '1':
        print aes.encrypt(hashstr)
    elif crypttype == '2':
        print aes.decrypt(hashstr).decode('utf-8')