import rsa
import log

class Wallet:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(256)
        log.info("Created wallet!")
        log.info("PUBLIC KEY: " + str(self.public_key))
        log.info("PRIVATE KEY: " + str(self.private_key))
        log.warn("Don't share your private key with anyone!")