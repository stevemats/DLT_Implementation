import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.chain = []  # List to hold the blockchain
        self.current_transactions = []  # List to hold pending transactions
        # Create the genesis block
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,  # Index of the new block
            'timestamp': time(),  # Current timestamp
            'transactions': self.current_transactions,  # Transactions in the new block
            'proof': proof,  # Proof of work for the new block
            # Previous block's hash
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []  # Reset the list of pending transactions
        self.chain.append(block)  # Append the new block to the chain
        return block  # Return the new block

    # Method to add a new transaction to the list of pending transactions
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,  # Sender of the transaction
            'recipient': recipient,  # Recipient of the transaction
            'amount': amount,  # Amount of the transaction
        })
        # Return the index of the new block
        return self.last_block['index'] + 1

    # Static method to calculate the hash of a block
    @staticmethod
    def hash(block):
        # Convert the block to a string and encode it
        block_string = json.dumps(block, sort_keys=True).encode()
        # Return the SHA-256 hash of the block
        return hashlib.sha256(block_string).hexdigest()

    # Property to get the last block in the chain
    @property
    def last_block(self):
        # Return the last block if the chain is not empty
        return self.chain[-1] if len(self.chain) > 0 else None

    # Method to save the blockchain to a JSON file
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chain, f)

    # Method to load the blockchain from a JSON file
    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.chain = json.load(f)


# Create a new Blockchain instance
blockchain = Blockchain()

while True:
    print(" ")
    print("=======================")
    print("Block of Chains ~ Steve")
    print("=======================")
    print("""
    |>>>                                                      |>>>
    |                     |>>>          |>>>                  |
    *                     |             |                     *
   / \                    *             *                    / \\
  /___\                 _/ \           / \_                 /___\\
  [   ]                |/   \_________/   \|                [   ]
  [ I ]                /     \       /     \                [ I ]
  [   ]_ _ _          /       \     /       \          _ _ _[   ]
  [   ] U U |        {#########}   {#########}        | U U [   ]
  [   ]====/          \=======/     \=======/          \====[   ]
  [   ]    |           |   I |_ _ _ _| I   |           |    [   ]
  [___]    |_ _ _ _ _ _|     | U U U |     |_ _ _ _ _ _|    [___]
  \===/  I | U U U U U |     |=======|     | U U U U U | I  \===/
   \=/     |===========| I   | + W + |   I |===========|     \=/
    |  I   |           |     |_______|     |           |   I  |
    |      |           |     |||||||||     |           |      |
    |      |           |   I ||vvvvv|| I   |           |      |
_-_-|______|-----------|_____||     ||_____|-----------|______|-_-_
   /________\         /______||     ||______\         /________\\
  |__________|-------|________\_____/________|-------|__________|
        """)
    print("Choose a Menu Item Below to Proceed:")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Add Transaction")
    print("2. View Blockchain")
    print("3. Mine Block")
    print("4. Save Blockchain")
    print("5. Load Blockchain")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        sender = input("Enter sender: ")
        recipient = input("Enter recipient: ")
        amount = input("Enter amount: ")
        blockchain.new_transaction(sender, recipient, amount)
        print("Transaction added successfully.")

    elif choice == '2':
        print(json.dumps(blockchain.chain, indent=4))

    elif choice == '3':
        proof = 0  # Initialize the proof of work to 0
        max_iterations = 10000  # Set a lower maximum number of iterations
        for _ in range(max_iterations):
            # Check if the hash of the last block starts with '0'
            if blockchain.hash(blockchain.last_block).startswith('0'):
                break  # If it does, exit the loop
            proof += 1  # Increment the proof of work

        # If a valid proof of work is found, add the new block to the chain
        if proof < max_iterations:
            blockchain.new_block(proof)
            print("Block mined successfully.")
        else:
            print("Proof of work not found within the maximum number of iterations.")

    elif choice == '4':
        filename = input("Enter filename to save blockchain: ")
        blockchain.save_to_file(filename)
        print(f"Blockchain saved to {filename}.")

    elif choice == '5':
        filename = input("Enter filename to load blockchain: ")
        blockchain.load_from_file(filename)
        print(f"Blockchain loaded from {filename}.")

    elif choice == '6':
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please try again.")
