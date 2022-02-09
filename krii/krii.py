from argparse import ArgumentParser

from blockchain import Blockchain
from node import Node

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int, help="port to listen on")
    args = parser.parse_args()
    port = args.port

    blockchain = Blockchain()

    node = Node(port, blockchain)
    node.run()