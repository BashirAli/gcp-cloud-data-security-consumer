import gnupg
import argparse
import os
import logging

def generate_gpg_keys(name: str, email: str, passphrase: str, key_length: int, output_dir: str) -> None:
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialise GnuPG
    gpg = gnupg.GPG()

    # Define key params
    key_params = {
        'key_type': 'RSA',
        'key_length': key_length,
        'name_real': name,
        'name_email': email,
        'passphrase': passphrase
    }

    # Generate key pair
    logging.info("Generating GPG key pair.")
    key = gpg.gen_key(gpg.gen_key_input(**key_params))

    if key:
        logging.info(f"Key generation successful! Key Fingerprint: {key.fingerprint}")

        # Export Public Key as ASCII text
        public_key_file: str = os.path.join(output_dir, "public_key.txt")
        with open(public_key_file, "w") as f:
            f.write(gpg.export_keys(key.fingerprint, armor=True))  # ASCII format

        # Export Private Key as ASCII text
        private_key_file: str = os.path.join(output_dir, "private_key.txt")
        with open(private_key_file, "w") as f:
            f.write(gpg.export_keys(key.fingerprint, secret=True, passphrase=passphrase, armor=True))  # ASCII format
    else:
        logging.error("Key generation failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a GPG key pair with a passphrase.")

    parser.add_argument("--name", required=True, help="Real name of the key owner.")
    parser.add_argument("--email", required=True, help="Email address for the key.")
    parser.add_argument("--passphrase", required=True, help="Passphrase for securing the private key.")
    parser.add_argument("--key-length", type=int, default=2048, help="RSA key length (default: 2048).")
    parser.add_argument("--output-dir", default=os.getcwd(),
                        help="Directory to save the keys (default: current directory).")

    args = parser.parse_args()

    generate_gpg_keys(args.name, args.email, args.passphrase, args.key_length, args.output_dir)
