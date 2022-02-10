from flask import Flask, jsonify, request, redirect, send_from_directory
from flask_cors import CORS
from uuid import uuid4

class Server:
    def __init__(self, port, blockchain):
        self.port = port
        self.blockchain = blockchain
        self.nodes = []
        self.id = str(uuid4()).replace("-", "")
        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route("/")
        def base():
            return redirect("/admin")

        @self.app.route("/admin")
        def admin():
            return send_from_directory("admin/public", "index.html")

        @self.app.route("/<path:path>")
        def home(path):
            return send_from_directory("admin/public", path)

        @self.app.route("/blocks", methods=["GET"])
        def blocks():
            response = {
                "blocks": blockchain.blocks
            }

            return jsonify(response), 200

        @self.app.route("/transactions", methods=["GET"])
        def transactions():
            response = {
                "transactions": blockchain.transactions
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

    def add_node(self, address):
        url = urlparse(address)

        if url.netloc:
            self.nodes.append(url.netloc)
        elif url.path:
            self.nodes.append(url.path)
        else:
            raise ValueError("Invalid URL")

    def resolve_conflicts(self):
        replaced = False

        for node in self.nodes:
            response = requests.get(f"http://{node}/blocks")

            if response.status_code == 200:
                chain = response.json()["blocks"]

                if len(chain) > len(self.blocks) and self.valid_chain(chain):
                    self.blocks = chain
                    replaced = True

    def run(self):
        self.app.run(host="0.0.0.0", port=self.port)