from ecdsa import SigningKey
import log

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.verifying_key

        log.info("Created wallet!")
        log.info("PUBLIC KEY: " + self.public_key.to_string().hex())
        log.info("PRIVATE KEY: " + self.private_key.to_string().hex())
        log.warn("Don't share your private key with anyone!")