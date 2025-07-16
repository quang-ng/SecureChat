
# SecureChat

SecureChat is a lightweight, bidirectional chat application built with Python sockets, featuring hybrid RSA + AES encryption for secure communication.

## Features
- End-to-end encrypted chat using hybrid RSA (for key exchange) and AES (for message encryption)
- Simple command-line interface for both server and client
- Easy RSA key generation tool

## Getting Started

### 1. Install dependencies
```sh
pip install -r requirements.txt
```

### 2. Generate RSA key pair
```sh
python -m securechat.utils.keygen
```
This creates `server_private.pem` and `server_public.pem` in your current directory.

### 3. Start the server
```sh
python -m securechat.server
```

### 4. Start the client (in a new terminal)
```sh
python -m securechat.client
```

- Make sure `server_public.pem` is present in the client directory.
- Make sure `server_private.pem` is present in the server directory.

## How it works
- The client generates a random AES session key.
- The client encrypts the AES key with the server's RSA public key and sends it to the server.
- Both client and server use the AES key to encrypt/decrypt all chat messages.

## File structure
- `securechat/server.py` — Server code
- `securechat/client.py` — Client code
- `securechat/crypto/rsa_utils.py` — RSA key and encryption utilities
- `securechat/crypto/aes_utils.py` — AES encryption utilities
- `securechat/utils/keygen.py` — CLI tool for RSA key generation

## License
MIT
