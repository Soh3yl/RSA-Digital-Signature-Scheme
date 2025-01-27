import os
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature


class RSADigitalSignature:
    def __init__(self, key_size=2048):

        self.key_size = key_size
        self.private_key = None
        self.public_key = None

    def generate_key_pair(self, key_path='./'):

        os.makedirs(key_path, exist_ok=True)

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )
        self.public_key = self.private_key.public_key()

        private_key_path = os.path.join(
            key_path, 'private_key.pem')
        public_key_path = os.path.join(
            key_path, 'public_key.pem')

        with open(private_key_path, 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(public_key_path, 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        return private_key_path, public_key_path

    def sign_file(self, file_path, signature_path=None):

        if not self.private_key:
            raise ValueError(
                "Key pair not generated. Call generate_key_pair() first.")

        with open(file_path, 'rb') as f:
            file_data = f.read()

        sha3_hash = hashlib.sha3_256(file_data).digest()

        signature = self.private_key.sign(
            sha3_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA3_256()
        )

        if signature_path:
            with open(signature_path, 'wb') as f:
                f.write(signature)

        return signature

    def verify_signature(self, file_path, signature_path, public_key_path=None):
        if public_key_path and not self.public_key:
            with open(public_key_path, 'rb') as f:
                self.public_key = serialization.load_pem_public_key(f.read())

        if not self.public_key:
            raise ValueError("Public key not loaded. Provide public key path.")

        with open(file_path, 'rb') as f:
            file_data = f.read()

        with open(signature_path, 'rb') as f:
            signature = f.read()

        sha3_hash = hashlib.sha3_256(file_data).digest()

        try:
            self.public_key.verify(
                signature,
                sha3_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA3_256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA3_256()
            )
            return True
        except InvalidSignature:
            return False
