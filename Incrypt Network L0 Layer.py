import hashlib
import time

def proof_of_work(last_proof, difficulty):
    exponent = difficulty
    while True:
        guess = (str(time.time()) + str(last_proof)).encode('utf-8')
        guess_hash = hashlib.sha256(guess).hexdigest()
        if guess_hash[:exponent] == '0' * exponent:
            return guess_hash

last_proof = 0
difficulty = 5

for i in range(10):
    last_proof = proof_of_work(last_proof, difficulty)
    print("New proof found: ", last_proof)