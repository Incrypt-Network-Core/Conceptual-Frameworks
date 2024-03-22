import hashlib
import time
import tensorflow as tf
import json
from flask import Flask, request, jsonify

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0" * 64, int(time.time()), "Genesis Block", self.calculate_hash(0, "0" * 64, 0, "Genesis Block"))

    def calculate_hash(self, index, previous_hash, timestamp, data, nonce=0):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(nonce)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def proof_of_work(self, last_proof, difficulty):
        exponent = difficulty
        while True:
            guess = (str(time.time()) + str(last_proof)).encode('utf-8')
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash[:exponent] == '0' * exponent:
                return guess_hash

    def add_block(self, block):
        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block.index, previous_block.hash, current_block.timestamp, current_block.data, current_block.nonce):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# AI model
model = tf.keras.models.load_model("my_model.h5")

# Flask app for API
app = Flask(__name__)

# Global blockchain variable
blockchain = Blockchain()

# Route for mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    last_block = blockchain.chain[-1]
    last_proof = last_block.nonce
    difficulty = blockchain.difficulty

    proof = blockchain.proof_of_work(last_proof, difficulty)

    blockchain.pending_transactions.append({
        'sender': '0',
        'receiver': 'miner',
        'amount': 5,
        'ai_input': json.dumps({'data': [1, 2, 3, 4, 5]}),
        'ai_output': json.dumps(model.predict(tf.convert_to_tensor([[1, 2, 3, 4, 5]])))
    })

    block = Block(len(blockchain.chain), last_block.hash, int(time.time()), blockchain.pending_transactions, proof)
    blockchain.add_block(block)
    blockchain.pending_transactions = []

    return jsonify({'message': 'Block mined successfully!', 'index': block.index, 'hash': block.hash, 'transactions': block.data}), 200

# Start the Flask app
if __name__ == '__main__