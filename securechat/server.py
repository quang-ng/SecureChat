# server.py

import base64
import socket
import threading

from securechat.crypto.aes_utils import decrypt_aes, encrypt_aes
from securechat.crypto.rsa_utils import decrypt_rsa

HOST = 'localhost'   # Or use your local IP address for LAN
PORT = 5002


def receive_messages(conn, aes_key):
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            try:
                print(f"\nCipher message: {data}")
                decrypted = decrypt_aes(aes_key, data)
                print(f"\n👤 Client: {decrypted.decode()}\nYou: ", end="")
            except Exception as e:
                print(f"\n[!] Decryption error: {e}\nYou: ", end="")
        except Exception as e:
            print(f"\n[!] Error: {e}")
            break


def server_chat():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"🟢 Server listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    print(f"🔌 Connected by {addr}")

    # --- Hybrid Key Exchange ---
    # 1. Load server's private key (assume it's in 'server_private.pem')
    with open('server_private.pem', 'rb') as f:
        server_privkey = f.read()

    # 2. Receive encrypted AES key from client
    while True:
        data = conn.recv(4096)
        if data.startswith(b'KEY:'):
            encrypted_aes_key = data[4:]
            print("encrypted_aes_key from client: ", encrypted_aes_key)
            aes_key = decrypt_rsa(server_privkey, encrypted_aes_key)
            break
    print("[+] AES session key received and decrypted.")

    # Start receiving thread with AES key
    threading.Thread(target=receive_messages, args=(conn, aes_key), daemon=True).start()

    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            conn.close()
            break
        encrypted_msg = encrypt_aes(aes_key, msg.encode())
        conn.sendall(encrypted_msg)

if __name__ == "__main__":
    server_chat()
