import hashlib
import json
from time import time

from config import config
from db import Db
import log

log.to_file = False

class Blockchain:
    def __init__(self):
        self.transactions_db = Db(config["transactions_db_name"])
        self.blocks_db = Db(config["blocks_db_name"])

        self.transactions = self.transactions_db.read() or []
        self.blocks = self.blocks_db.read() or []

        self.mining_difficulty = config["mining_difficulty"]
        self.mining_reward = config["mining_reward"]

        if len(self.blocks) == 0:
            self.add_genesis()
            log.info("Created genesis block beacause chain was empty")

    # TRANSACTIONS (TO TEST)
    def new_transaction(self, sender, recipient, amount):
        new_transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time()
        }

        return new_transaction

    def calculate_transaction_hash(self, transaction):
        return hashlib.sha256(f"{transaction['sender']}{transaction['recipient']}{transaction['amount']}{transaction['timestamp']}".encode()).hexdigest()

    def check_transaction(self, transaction):
        if not transaction["signature"]:
            log.warn("No signature in this transaction")
            return False
        if not transaction["sender"].verify(self.calculate_transaction_hash(transaction), transaction["signature"]):
            log.warn("Invalid transaction signature")
            return False

        return True

    def sign_transaction(self, transaction, private_key):
        if private_key.verifying_key.to_string().hex() != transaction["sender"]:
            log.error("Cannot sign transactions for other addresses")
            return

        transaction["signature"] = private_key.sign(self.calculate_transaction_hash(transaction))

    def add_transaction(self, transaction):
        if not transaction["sender"] or not transaction["recipient"]:
            log.error("Transaction must include sender and recipient")
            return
        elif transaction["amount"] <= 0:
            log.error("Transaction amount should be higher than 0")
            return
        elif not self.check_transaction(transaction):
            log.error("Cannot add invalid transaction")
            return
















    def calculate_block_hash(self, block):
        return hashlib.sha256(f"{block['index']}{block['previous_hash']}{block['timestamp']}{json.dumps(block['transactions'])}{block['nonce']}".encode()).hexdigest()

    def check_block(self, block, previous_block):
        if previous_block["index"] + 1 != block["index"]:
            log.error("Error")
            return False
        elif previous_block["hash"] != block["previous_hash"]:
            log.error("Error")
            return False
        elif self.calculate_block_hash(block) != block["hash"]:
            log.error("Error")
            return False
        elif block["hash"][:config["mining_difficulty"]] != "0" * config["mining_difficulty"]:
            log.error("Error")
            return False

        for transaction in block["transactions"]:
            if not check_transaction(transaction):
                log.error("Error")
                return False

        return True

    def add_block(self, previous_hash):
        new_block = {
            "index": len(self.blocks) + 1,
            "previous_hash": previous_hash,
            "timestamp": time(),
            "transactions": self.transactions,
            "nonce": 0,
            "hash": None
        }

        new_block["hash"] = self.calculate_block_hash(new_block)

        if self.check_block(new_block, self.blocks[-1]):
            self.blocks.append(new_block)
            self.blocks_db.write(self.blocks)

            self.transactions = []
            self.transactions_db.write(self.transactions)
        else:
            log.error("Invalid block")

    def add_genesis(self):
        self.blocks.append({
            "index": 1,
            "previous_hash": "Genesis",
            "timestamp": time(),
            "transactions": [],
            "nonce": 0
        })

        self.blocks_db.write(self.blocks)

    def check_chain(self, chain):
        for block in chain:
            if not self.check_block(block, chain.blocks[block["index"] - 1]):
                return False

        return True

    def replace_chain(self, chain):
        if len(chain) <= len(self.blocks):
            log.error("Blockchain shorter")
            return False

        if not self.check_chain(chain):
            log.error("Blockchain invalid")
            return False

        self.blocks = chain
        self.blocks_db.write(self.blocks)

        return True

    def print(self):
        for block in self.blocks:
            print(json.dumps(block, indent=4))