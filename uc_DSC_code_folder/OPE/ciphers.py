##################################################################
# This file is part of the POPE implementation.                  #
# Paper at https://eprint.iacr.org/2015/1106                     #
# U.S. Government work product, in the public domain.            #
# Written in 2015 by Daniel S. Roche, roche@usna.edu             #
##################################################################

"""
Ciphers for use with an OPE oracle.
"""

import Crypto.Hash.MD5
import Crypto.Cipher.AES
import Crypto.Random
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

class DumbCipher:
    """This dumb cipher just appends the key to the end of the ciphertext."""

    def __init__(self, key):
        self.key = "DumbKey" if key is None else key

    def encode(self, s):
        return str(s)[::-1] + '|' + self.key

    def decode(self, s):
        if s.endswith('|'+self.key):
            return s[-len(self.key)-2::-1]
        else:
            raise ValueError("wrong decryption key for {}: {}".format(s, self.key))


class AES_ECB:
    """一个用于封装PyCryptodome的AES128 ECB密码"""

    def __init__(self, key=None):
        self.key = key
        if self.key:
            self.realkey = MD5.new(self.key.encode('utf-8')).digest()
        else:
            self.realkey = Random.new().read(16)
        self.ciph = AES.new(self.realkey, AES.MODE_ECB)

    def encode(self, plaintext):
        plaintext_bytes = plaintext.encode('utf-8')
        plaintext_padded = pad(plaintext_bytes, AES.block_size)
        ciphertext_bytes = self.ciph.encrypt(plaintext_padded)
        return ciphertext_bytes.hex()

    def decode(self, ciphertext_hex):
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        plaintext_padded = self.ciph.decrypt(ciphertext_bytes)
        plaintext_bytes = unpad(plaintext_padded, AES.block_size)
        return plaintext_bytes.decode('utf-8')


class AES_ECB_192:
    """用于封装192位AES密码的类"""

    def __init__(self, key=None):
        if key:
            # MD5哈希后的结果是16字节，将其扩展到24字节
            hashed_key = MD5.new(key.encode('utf-8')).digest()
            if len(hashed_key) != 16:
                raise ValueError("Invalid key length after MD5 hash. Key must be 16 bytes.")
            self.realkey = hashed_key + hashed_key[:8]  # 扩展至24字节
            # 确保密钥是24字节（192位）
            if len(self.realkey) != 24:
                raise ValueError("Invalid key length for AES-192. Key must be 24 bytes.")
        else:
            self.realkey = Random.new().read(24)

        self.ciph = AES.new(self.realkey, AES.MODE_ECB)

    def encode(self, plaintext):
        plaintext_bytes = plaintext.encode('utf-8')
        plaintext_padded = pad(plaintext_bytes, AES.block_size)
        ciphertext_bytes = self.ciph.encrypt(plaintext_padded)
        return ciphertext_bytes.hex()

    def decode(self, ciphertext_hex):
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        plaintext_padded = self.ciph.decrypt(ciphertext_bytes)
        plaintext_bytes = unpad(plaintext_padded, AES.block_size)
        return plaintext_bytes.decode('utf-8')


class AES_ECB_256:
    """用于封装256位AES密码的类"""

    def __init__(self, key=None):
        if key:
            # MD5哈希后的结果是16字节，将其扩展到32字节
            hashed_key = MD5.new(key.encode('utf-8')).digest()
            if len(hashed_key) != 16:
                raise ValueError("Invalid key length after MD5 hash. Key must be 16 bytes.")
            self.realkey = hashed_key + hashed_key  # 扩展至32字节
            # 确保密钥是32字节（256位）
            if len(self.realkey) != 32:
                raise ValueError("Invalid key length for AES-256. Key must be 32 bytes.")
        else:
            self.realkey = Random.new().read(32)

        self.ciph = AES.new(self.realkey, AES.MODE_ECB)

    def encode(self, plaintext):
        plaintext_bytes = plaintext.encode('utf-8')
        plaintext_padded = pad(plaintext_bytes, AES.block_size)
        ciphertext_bytes = self.ciph.encrypt(plaintext_padded)
        return ciphertext_bytes.hex()

    def decode(self, ciphertext_hex):
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        plaintext_padded = self.ciph.decrypt(ciphertext_bytes)
        plaintext_bytes = unpad(plaintext_padded, AES.block_size)
        return plaintext_bytes.decode('utf-8')