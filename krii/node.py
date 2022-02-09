from flask import Flask, jsonify, request
from uuid import uuid4

class Node:
    def __init__(self, port, blockchain):
        self.port = port
        self.blockchain = blockchain
        self.id = str(uuid4()).replace("-", "")
        self.app = Flask(__name__)

        @self.app.route("/blocks", methods=["GET"])
        def blocks():
            response = {
                "blocks": blockchain.blocks
            }

            return jsonify(response), 200

        @self.app.route("/transactions", methods=["GET"])
        def transactions():
            response = {
                "transactions": blockchain.pending_transactions
            }

            return jsonify(response), 200

        @self.app.route("/nodes", methods=["GET"])
        def nodes():
            response = {
                "nodes": blockchain.nodes
            }

            return jsonify(response), 200

        @self.app.route("/transactions/new", methods=["POST"])
        def transactions_new():
            values = request.get_json()

            required = ["sender", "recipient", "amount"]
            if not all(k in values for k in required):
                return "Missing values", 400

            blockchain.add_transaction(values["sender"], values["recipient"], values["amount"])

            response = {"message": "Transaction will soon be added."}

            return jsonify(response), 201

        @self.app.route("/mine", methods=["POST"])
        def mine():
            mined = blockchain.mine("test")

            return jsonify(mined), 201

        @self.app.route("/nodes/register", methods=["POST"])
        def nodes_register():
            values = request.get_json()

            nodes = values.get("nodes")
            if nodes is None:
                return "Please supply valid nodes list", 400

            for node in nodes:
                blockchain.add_node(node)

            return "Added nodes", 201

        @self.app.route("/nodes/resolve", methods=["GET"])
        def nodes_resolve():
            replaced = blockchain.resolve_conflicts()

            if replaced:
                return "Our chain was replaced", 200
            else:
                return "Our chain is authorative", 200

    def run(self):
        self.app.run(host="0.0.0.0", port=self.port)