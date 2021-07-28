from builtins import bytes
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

class InvalidTokenError(Exception):
    pass

class PasswordManager:

    @staticmethod
    def get_key(password):  # Generate a 32 bit key from the user given key

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(password)
        return base64.urlsafe_b64encode(digest.finalize())

    def __init__(self, password):
        self.fernet = Fernet( self.get_key(password.encode("utf-8")))


    def decrypt(self, data):
        try:
            if type(data) != bytes:
                data = bytes(data.encode("utf-8"))

            return self.fernet.decrypt(data)
        except InvalidToken:
            raise  InvalidTokenError

    def encrypt(self, data):
        if type(data) != bytes:
            data = bytes(data.encode("utf-8"))

        return self.fernet.encrypt(data)

