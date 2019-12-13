import os
import ecdsa
import base64
import hashlib
import binascii


class SignKey(object):
    def __init__(self, private_key):
        """
        Initialize a private key.
        :param private_key: Private key file path
        """
        self._private_key = self._load_private_key(private_key)
        self._public_key = self._private_key.get_verifying_key()

    def get_key_id(self):
        """Get unique Monobank identifier (X-Key-Id)"""
        uncompressed_public_key = bytearray([0x04]) + (bytearray(self._public_key.to_string()))
        return binascii.hexlify(hashlib.sha256(uncompressed_public_key).digest())

    def sign(self, data):
        """
        Signs string data with private key, and hash(sha256)
        :param data: A string to be signed
        :return: Signed string
        """
        sign = self._private_key.sign(data.encode(), hashfunc=hashlib.sha256)
        return base64.b64encode(sign)

    def _load_private_key(self, private_key):
        if 'PRIVATE KEY-----' in private_key:
            raw = self.private_key
        elif os.path.exists(private_key):
            with open(private_key) as f:
                raw = f.read()
        else:
            raise Exception('Cannot load private key')
        return ecdsa.SigningKey.from_pem(raw)
