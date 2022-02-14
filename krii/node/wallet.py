from ecdsa import SigningKey, SECP256k1
import log

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.pubk = self.private_key.verifying_key

        self.public_key = self.pubk.to_string().hex()

        log.info("Created wallet!")
        log.info("PUBLIC KEY: " + self.public_key)
        log.info("PRIVATE KEY: " + self.private_key.to_string().hex())
        log.warn("Don't share your private key with anyone!")