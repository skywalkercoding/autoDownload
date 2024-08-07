from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
from cryptography.hazmat.primitives import serialization

class EncryptedKey():

    def extract_modulus_exponent(self,public_key_str):
        # 解码Base64字符串
        public_key_bytes = base64.b64decode(public_key_str)

        try:
            # 尝试使用DER格式加载
            public_key = serialization.load_der_public_key(public_key_bytes, backend=default_backend())
        except ValueError:
            # 如果加载失败，则尝试使用PEM格式加载
            public_key = serialization.load_pem_public_key(public_key_bytes,
                                                                 backend=default_backend()).public_key()

        # 获取公钥的模数和指数
        modulus = public_key.public_numbers().n
        exponent = public_key.public_numbers().e

        return modulus, exponent
    def create_key_from_string(self,public_key_str):
        public_key_bytes = base64.b64decode(public_key_str)

        # 尝试使用PEM格式加载公钥
        try:
            public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
        except ValueError:
            # 如果加载失败，则尝试使用DER格式加载
            public_key = serialization.load_der_public_key(public_key_bytes, backend=default_backend())

        return public_key

    def encrypt_string(self,data, pubkey):
        key = self.create_key_from_string(pubkey)

        # Convert the data to bytes
        data_bytes = data.encode('utf-8')

        # Encrypt the data
        ciphertext = b""
        while data_bytes:
            chunk = data_bytes[:86]
            data_bytes = data_bytes[86:]

            # Use OAEP padding
            ciphertext += key.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None
                )
            )

        # Base64 encode the encrypted data
        encrypted_base64 = base64.b64encode(ciphertext).decode('utf-8')
        return encrypted_base64


