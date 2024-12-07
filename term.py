import hashlib
import time

# Block class to define a block in the blockchain
class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Blockchain class to manage the blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), "Genesis Block", 0)
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.is_valid_proof(last_proof, proof):
            proof += 1
        return proof

    def is_valid_proof(self, last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Example difficulty level

    def add_block(self, proof, data):
        last_block = self.get_last_block()
        new_block = Block(
            index=len(self.chain),
            previous_hash=last_block.calculate_hash(),
            timestamp=time.time(),
            data=data,
            proof=proof,
        )
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.calculate_hash():
                return False
            if not self.is_valid_proof(previous.proof, current.proof):
                return False
        return True

# User interactions
class User:
    def __init__(self, username):
        self.username = username

    def send_transaction(self, blockchain, recipient, amount):
        transaction = f"{self.username} -> {recipient}: {amount}"
        blockchain.pending_transactions.append(transaction)

# Main simulation
if __name__ == "__main__":
    blockchain = Blockchain()
    user1 = User("Alice")
    user2 = User("Bob")
    user1 = User("Mahesh")
    user2 = User("Venkatesh")
    

    # Users send transactions
    user1.send_transaction(blockchain, "Bob", 50)
    user2.send_transaction(blockchain, "Alice", 30)
    user1.send_transaction(blockchain, "Venkatesh", 50)
    user2.send_transaction(blockchain, "Mahesh", 30)

    # Mining a new block
    print("Mining a new block...")
    proof = blockchain.proof_of_work(blockchain.get_last_block().proof)
    blockchain.add_block(proof, blockchain.pending_transactions)
    blockchain.pending_transactions = []

    # Validate the chain
    print("Is the blockchain valid?", blockchain.validate_chain())

    # Display the blockchain
    for block in blockchain.chain:
        print(f"Block {block.index} [Hash: {block.calculate_hash()}]")
        print(f"Previous: {block.previous_hash}")
        print(f"Data: {block.data}")
        print(f"Proof: {block.proof}")
        print()
