import gnupg
import argparse
import os
import logging

def encrypt_json(json_file: str, public_key_file: str) -> None:
    if not os.path.isfile(json_file):
        logging.error(f"Error: JSON file '{json_file}' does not exist.")
        return
    if not os.path.isfile(public_key_file):
        logging.error(f"Error: Public key file '{public_key_file}' does not exist.")
        return

    # Initialise GnuPG
    gpg = gnupg.GPG()

    # Import key
    with open(public_key_file, "rb") as key_file:
        import_result = gpg.import_keys(key_file.read())

    if not import_result.fingerprints:
        print("Error: Failed to import the public key.")
        return

    fingerprint = import_result.fingerprints[0]
    print(f"Successfully imported public key with fingerprint: {fingerprint}")

    # Read JSON content
    with open(json_file, "rb") as f:
        json_data = f.read()

    # Encrypt JSON
    encrypted_data = gpg.encrypt(json_data, recipients=[fingerprint], always_trust=True)

    if not encrypted_data.ok:
        logging.error("Error: Encryption failed.")
        logging.error("GPG Error Message:", encrypted_data.stderr)
        return

    # Save encrypted file as .json.gpg
    encrypted_file = f"{json_file}.gpg"
    with open(encrypted_file, "wb") as f:
        f.write(encrypted_data.data)

    logging.info(f"Encryption successful! Encrypted file saved as: {encrypted_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt a JSON file using a GPG public key.")

    parser.add_argument("--json-file", required=True, help="Path to the JSON file to encrypt.")
    parser.add_argument("--public-key", required=True, help="Path to the GPG public key file.")

    args = parser.parse_args()

    encrypt_json(args.json_file, args.public_key)
