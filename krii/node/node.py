from argparse import ArgumentParser

from blockchain import Blockchain
from server import Server
from wallet import Wallet

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int, help="port to listen on")
    args = parser.parse_args()
    port = args.port

    blockchain = Blockchain()

    vinny = Wallet()
    giorgio = Wallet()
    andrea = Wallet()


    # Initial coin distribution

    blockchain.transactions.append(blockchain.new_transaction(None, vinny.public_key, 100))
    blockchain.mine_pending_transactions(giorgio.public_key)

    server = Server(port, blockchain)
    server.run()