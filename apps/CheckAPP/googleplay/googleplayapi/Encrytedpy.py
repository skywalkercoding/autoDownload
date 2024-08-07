import base64
import hashlib

from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey.RSA import RsaKey
from gpsoauth.google import key_to_struct


class EncrytedPy():

    def construct_signature(self,email: str, password: str, key: RsaKey) -> bytes:
        """Construct signature."""
        signature = bytearray(b"\x00")

        struct = key_to_struct(key)
        signature.extend(hashlib.sha1(struct).digest()[:4])

        cipher = PKCS1_OAEP.new(key)
        encrypted_login = cipher.encrypt((email + "\x00" + password).encode("utf-8"))

        signature.extend(encrypted_login)

        return base64.urlsafe_b64encode(signature)
