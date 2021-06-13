# Module 1 - Create a Blockchain
# To be installed: 
# Flask : pip install Flask==0.12.2
# Postman: HTTP Client : https://www.getpostman.com

#Imprting the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

 #Building a block Chain
 
class Blockchain:
     
    def __init__(self):
         self.chain = []
         self.create_block(proof = 1, previous_hash = '0')

         
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash
                 }
        self.chain.append(block)
        return block;
    def get_previous_block(self):
        return self.chain[-1]
    
    def  proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof - previous_proof).encode()).hexdigest()
            if hash_operation[0:4] == "0000":
                check_proof = True
            else:
                new_proof +=1
        return new_proof
                
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_Chain_Valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            if hashlib.sha256(str(block['proof'] - previous_block['proof']).encode()).hexdigest()[0:4] != '0000':
                return False
            previous_block = block
            block_index +=1
        return True;
         
 
 
 #Mining a block Chain

#Creating a Web app

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# adding a block

blockchain = Blockchain()

# Mining a new block

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof  = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, blockchain.hash(previous_block))
    response = {'message' : 'Congrats you just mined a block',
                'index': block['index'],
                 'timestamp' : block['timestamp'],
                 'proof' : block['proof'],
                 'previous_hash' : block['previous_hash']
                }
    return jsonify(response), 200
    
# Getting the full block chain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'len' : len(blockchain.chain)
                }
    return jsonify(response), 200

# Check if blockchain is Valid or not
@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = {'isValid' : blockchain.is_Chain_Valid(blockchain.chain)}
    return jsonify(response),200

# Running the app

app.run(host='0.0.0.0', port=5000)