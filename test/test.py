import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RSA_Digital_Signature.RSADigitalSignature import RSADigitalSignature

signature_system = RSADigitalSignature()

private_key_path, public_key_path = signature_system.generate_key_pair()
print(f"Private key saved to: {private_key_path}")
print(f"Public key saved to: {public_key_path}")

# Create a text file to sign
with open('test/unsigned_text/text_to_sign.txt', 'w') as f:
    f.write("This is a confidential document wrote by Soheyl that needs to be digitally signed.")

# Sign the file
signature_path = 'test/signature_path/signed_text.txt'
signature = signature_system.sign_file(
    'test/unsigned_text/text_to_sign.txt', signature_path)
print(f"File signed. Signature saved to: {signature_path}")

# Verify the signature
is_valid = signature_system.verify_signature(
    'test/unsigned_text/text_to_sign.txt', signature_path, 'public_key.pem')
print(f"Signature verification: {'Valid' if is_valid else 'Invalid'}")
