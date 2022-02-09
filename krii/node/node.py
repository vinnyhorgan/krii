from argparse import ArgumentParser

from blockchain import Blockchain
from server import Server

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int, help="port to listen on")
    args = parser.parse_args()
    port = args.port

    blockchain = Blockchain()

    server = Server(port, blockchain)
    server.run()