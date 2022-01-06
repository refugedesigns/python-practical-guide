import functools
import hashlib
import json
import pickle
from block import Block
from transaction import Transaction
from utility.hash_util import hash_block
from utility.verification import Verification
from wallet import Wallet

# The reward we give to miners (for creating a new block)
MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id) -> None:
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.__chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        self.hosting_node = hosting_node_id
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open("blockchain.txt", mode="r") as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [
                        Transaction(tx['sender'], tx["recipient"],
                                    tx['signature'], tx["amount"])
                        for tx in block["transactions"]
                    ]
                    updated_block = Block(block["index"],
                                          block["previous_hash"], converted_tx,
                                          block["proof"], block["timestamp"])
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_open_transactions = []
                for tx in open_transactions:
                    updated_tx = Transaction(tx["sender"], tx["recipient"],
                                             tx['signature'], tx["amount"])
                    updated_open_transactions.append(updated_tx)
                self.__open_transactions = updated_open_transactions
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                saveable_chain = [
                    block.__dict__ for block in [
                        Block(block_el.index, block_el.previous_hash,
                              [tx.__dict__ for tx in block_el.transactions],
                              block_el.proof, block_el.timestamp)
                        for block_el in self.__chain
                    ]
                ]
                f.write(json.dumps(saveable_chain))
                f.write("\n")
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
        except IOError:
            print("Saving failed!")

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    # This function accepts two arguments.
    # One required one (transaction_amount) and one optional one (last_transaction)
    # The optional one is optional because it has a default value => [1]

    def get_balance(self):
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [[
            tx.amount for tx in block.transactions if tx.sender == participant
        ] for block in self.__chain]
        open_tx_sender = [
            tx.amount for tx in self.__open_transactions
            if tx.sender == participant
        ]
        tx_sender.append(open_tx_sender)

        amount_sent = functools.reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
            if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

        tx_received = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]

        amount_received = functools.reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
            if len(tx_amt) > 0 else tx_sum + 0, tx_received, 0)

        return amount_received - amount_sent

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
            :sender: sender of the coin.
            :receiver: receiver of the coin.
            :amount: amount of the coind (default is 1 coin)
        """
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash,
                                           proof):
            proof += 1
        return proof

    def mined_block(self):
        """Create a new block and add open transactions to it."""
        if self.hosting_node == None:
            return None
        #Fetch the currently last block of the blockchain
        last_block = self.__chain[-1]
        #Hash the last block to be able to compare it to the stored hash
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        #Miners should be rewarded so lets create a reward transaction
        reward_transaction = Transaction("MINING", self.hosting_node, "",
                                         MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transactions(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions,
                      proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block
