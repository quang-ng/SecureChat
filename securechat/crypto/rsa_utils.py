
# RSA utility functions for SecureChat
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def generate_rsa_keypair(bits=2048):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_rsa(public_key_bytes, data):
    key = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(key)
    encrypted = cipher.encrypt(data)
    return base64.b64encode(encrypted)

def decrypt_rsa(private_key_bytes, enc):
    key = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(key)
    enc = base64.b64decode(enc)
    return cipher.decrypt(enc)
