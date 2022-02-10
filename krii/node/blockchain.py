import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

from config import config
from db import Db
import log

class Blockchain:
    def __init__(self):
        self.transactions_db = Db("transactions.json")
        self.blocks_db = Db("blocks.json")

        self.transactions = self.transactions_db.read() or []
        self.blocks = self.blocks_db.read() or []

        self.mining_difficulty = config["mining_difficulty"]
        self.mining_reward = config["mining_reward"]

        if len(self.blocks) == 0:
            self.add_genesis()
            log.info("Created genesis block beacause chain was empty")

    def calculate_transaction_hash(transaction):
        return hashlib.sha256(f"{transaction['sender']}{transaction['recipient']}{transaction['amount']}{transaction['timestamp']}".encode()).hexdigest()

    def check_transaction(transaction):
        pass






    def add_genesis(self):
        self.blocks.append({
            "index": 0,
            "timestamp": time(),
            "transactions": [],
            "proof": 0,
            "previous_hash": "Genesis"
        })

        self.blocks_db.write(self.blocks)

    def add_transaction(self, sender, recipient, amount):
        self.transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def add_block(self, proof):
        block = {
            "index": len(self.blocks) + 1,
            "timestamp": time(),
            "transactions": self.transactions,
            "proof": proof,
            "previous_hash": self.calculate_hash(self.blocks[-1])
        }

        self.transactions = []

        self.blocks.append(block)

        return block

    def proof_of_work(self):
        last_proof = self.blocks[-1]["proof"]
        last_hash = self.calculate_hash(self.blocks[-1])

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    def valid_proof(self, last_proof, proof, last_hash):
        difficulty_string = "0" * self.mining_difficulty

        guess = f"{last_proof}{proof}{last_hash}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        print("GUESS: " + guess_hash)

        return guess_hash[:self.mining_difficulty] == difficulty_string

    def mine(self, reward_address):
        proof = self.proof_of_work()

        self.add_transaction(
            sender="blockchain",
            recipient=reward_address,
            amount=self.mining_reward
        )

        mined = self.add_block(proof)

        return mined

    def print(self):
        for block in self.blocks:
            print(json.dumps(block, indent=4))

    def valid_chain(self, chain):
        index = 1

        while index < len(chain):
            block = chain[index]
            last_block = chain[index - 1]

            last_block_hash = self.calculate_hash(last_block)

            if block["previous_hash"] != self.calculate_hash(last_block):
                return False

            if not self.valid_proof(last_block["proof"], block["proof"], last_block_hash):
                return False

            index += 1

        return True

        return replaced