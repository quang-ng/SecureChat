# AES utility functions for SecureChat
import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def generate_aes_key(key_size=32):
    """Generate a random AES key (default 256 bits)."""
    return get_random_bytes(key_size)

def encrypt_aes(key, plaintext):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return base64.b64encode(cipher.nonce + tag + ciphertext)

def decrypt_aes(key, enc):
    enc = base64.b64decode(enc)
    nonce = enc[:16]
    tag = enc[16:32]
    ciphertext = enc[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
