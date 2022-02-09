import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

from db import Db

class Blockchain:
    def __init__(self):
        self.pending_transactions = []
        self.blocks = []
        self.mining_difficulty = 2
        self.mining_reward = 100
        self.nodes = []

        self.add_genesis()

    def add_genesis(self):
        self.blocks.append({
            "index": 0,
            "timestamp": time(),
            "transactions": [],
            "proof": 0,
            "previous_hash": "Genesis"
        })

    def add_node(self, address):
        url = urlparse(address)

        if url.netloc:
            self.nodes.append(url.netloc)
        elif url.path:
            self.nodes.append(url.path)
        else:
            raise ValueError("Invalid URL")

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def add_block(self, proof):
        block = {
            "index": len(self.blocks) + 1,
            "timestamp": time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": self.calculate_hash(self.blocks[-1])
        }

        self.pending_transactions = []

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

    def resolve_conflicts(self):
        replaced = False

        for node in self.nodes:
            response = requests.get(f"http://{node}/blocks")

            if response.status_code == 200:
                chain = response.json()["blocks"]

                if len(chain) > len(self.blocks) and self.valid_chain(chain):
                    self.blocks = chain
                    replaced = True

        return replaced

    def calculate_hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()