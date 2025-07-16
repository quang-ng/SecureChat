# client.py

import base64
import socket
import threading

from securechat.crypto.aes_utils import (decrypt_aes, encrypt_aes,
                                         generate_aes_key)
from securechat.crypto.rsa_utils import encrypt_rsa

HOST = 'localhost'   # Change to server's IP if connecting over LAN
PORT = 5002


def receive_messages(sock, aes_key):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            try:
                print(f"\nCipher message: {data}")
                decrypted = decrypt_aes(aes_key, data)
                print(f"\n👤 Server: {decrypted.decode()}\nYou: ", end="")
            except Exception as e:
                print(f"\n[!] Decryption error: {e}\nYou: ", end="")
        except Exception as e:
            print(f"\n[!] Error: {e}")
            break


def client_chat():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"🔗 Connected to server at {HOST}:{PORT}")

    # --- Hybrid Key Exchange ---
    # 1. Generate AES session key
    aes_key = generate_aes_key()

    # 2. Load server's public key (assume it's in 'server_public.pem')
    with open('server_public.pem', 'rb') as f:
        server_pubkey = f.read()

    # 3. Encrypt AES key with server's public key
    encrypted_aes_key = encrypt_rsa(server_pubkey, aes_key)
    # 4. Send encrypted AES key to server (prefix with b'KEY:')
    s.sendall(b'KEY:' + encrypted_aes_key)

    # Start receiving thread with AES key
    threading.Thread(target=receive_messages, args=(s, aes_key), daemon=True).start()

    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            s.close()
            break
        encrypted_msg = encrypt_aes(aes_key, msg.encode())
        s.sendall(encrypted_msg)

if __name__ == "__main__":
    client_chat()
