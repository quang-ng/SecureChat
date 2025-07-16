# CLI tool for SecureChat key generation
import argparse

from securechat.crypto.rsa_utils import generate_rsa_keypair


def main():
    parser = argparse.ArgumentParser(description="SecureChat Key Generation Tool")
    parser.add_argument('--out-public', default='server_public.pem', help='Output file for public key')
    parser.add_argument('--out-private', default='server_private.pem', help='Output file for private key')
    args = parser.parse_args()

    priv, pub = generate_rsa_keypair()
    with open(args.out_private, 'wb') as f:
        f.write(priv)
    with open(args.out_public, 'wb') as f:
        f.write(pub)
    print(f"Keys generated: {args.out_private}, {args.out_public}")

if __name__ == "__main__":
    main()
