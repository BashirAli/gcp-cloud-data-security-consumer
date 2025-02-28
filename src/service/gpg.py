from src.model.logging import logger
import gnupg

class GPGManager:

    def __init__(self):
        self.gpg_client = gnupg.GPG()
        self.passphrase = None

    def add_key_to_keyring(self, key_str:str):
        self.gpg_client.import_keys(key_data=key_str)
        key_str = self.gpg_client.list_keys()

        self.gpg_client.trust_keys(
            fingerprints=key_str[0]["fingerprint"], trustlevel="TRUST_ULTIMATE"
        )
        logger.info(msg="Incoming key added to keyring")

    def set_decrypt_passphrase(self, passphrase):
        self.passphrase = passphrase

    def decrypt_data(self, data: bytes) -> str:
        try:
            decrypted_data = self.gpg_client.decrypt(
                message=data, passphrase=self.passphrase
            )
            if not decrypted_data.ok:
                raise Exception(f"GPG Error - {decrypted_data.stderr}")

            return decrypted_data

        except Exception as e:
            logger.error(f"Cannot decrypt {data}\n Error Message: {e}")


