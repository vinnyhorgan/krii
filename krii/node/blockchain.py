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
            self.blocks.append(self.create_genesis())
            self.blocks_db.write(self.blocks)
            log.info("Created genesis block beacause chain was empty")

    # BLOCKCHAIN
    def create_genesis(self):
        genesis = {
            "previous_hash": "Genesis",
            "timestamp": time(),
            "transactions": [],
            "nonce": 0,
            "hash": ""
        }

        return genesis

    def check_chain(self):
        if self.create_genesis() != self.blocks[0]:
            return False

        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i - 1]

            if previous_block["hash"] != current_block["previous_hash"]:
                return False

            if not self.check_block(current_block):
                return False

            if current_block["hash"] != self.calculate_block_hash(current_block):
                return False

            return True

    def get_balance(self, address):
        balance = 0

        for block in self.blocks:
            for transaction in block["transactions"]:
                if transaction["sender"] == address:
                    balance -= transaction["amount"]

                if transaction["recipient"] == address:
                    balance += transaction["amount"]

        log.info(f"Balance of address {address} is: {balance}")
        return balance

    def mine_pending_transactions(self, reward_address):
        pending_transactions = self.transactions
        pending_transactions.append(self.new_transaction(None, reward_address, self.mining_reward))

        block = self.new_block(self.blocks[-1]["hash"], pending_transactions)
        self.mine_block(block)

        self.blocks.append(block)
        self.blocks_db.write(self.blocks)
        self.transactions = []

    # TRANSACTIONS
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

    def sign_transaction(self, transaction, private_key):
        if private_key.verifying_key != transaction["sender"]:
            log.error("Cannot sign transactions for other addresses")
            return

        #transaction["signature"] = private_key.sign(self.calculate_transaction_hash(transaction))

    def check_transaction(self, transaction):
        if transaction["sender"] == None:
            return True

        if "signature" not in transaction:
            log.warn("No signature in this transaction")
            return False
        if not transaction["sender"].verify(self.calculate_transaction_hash(transaction), transaction["signature"]):
            log.warn("Invalid transaction signature")
            return False

        return True

    def add_transaction(self, transaction):
        if "sender" not in transaction or "recipient" not in transaction:
            log.error("Transaction must include a sender and a recipient")
            return
        elif not self.check_transaction(transaction):
            log.error("Cannot add invalid transaction")
            return
        elif transaction["amount"] <= 0:
            log.error("Transaction amount should be higher than 0")
            return

        pending_amount = 0

        for tx in self.transactions:
            if tx["sender"] == transaction["sender"]:
                pending_amount += tx["amount"]

        total_balance = self.get_balance(transaction["sender"]) + pending_amount

        if total_balance < transaction["amount"]:
            log.error("Not enough balance!")
            return

        self.transactions.append(transaction)
        log.info("Added transaction!")

    # BLOCKS
    def new_block(self, previous_hash, transactions):
        new_block = {
            "previous_hash": previous_hash,
            "timestamp": time(),
            "transactions": transactions,
            "nonce": 0,
            "hash": ""
        }

        return new_block

    def calculate_block_hash(self, block):
        return hashlib.sha256(f"{block['previous_hash']}{block['timestamp']}{json.dumps(block['transactions'])}{block['nonce']}".encode()).hexdigest()

    def mine_block(self, block):
        while block["hash"][:self.mining_difficulty] != "0" * self.mining_difficulty:
            block["nonce"] += 1
            block["hash"] = self.calculate_block_hash(block)
            log.info(f"Trying hash: {block['hash']}")

        log.info(f"Block mined! Correct hash: {block['hash']}")

    def check_block(self, block):
        for transaction in block["transactions"]:
            if not self.check_transaction(transaction):
                return False

        return True