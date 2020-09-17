import hashlib

# class block:
#     def __init__(self,previous_hash,transction):
#         self.transaction=transction
#         self.previous_hash=previous_hash
#         string_to_hash="".join(transction)+previous_hash
#         print("String_To_hash:",string_to_hash)
#         self.block_hash=hashlib.sha256(string_to_hash.encode()).hexdigest()
#         #print(self.__dict__)
#############################################################################################
import json
from datetime import datetime
from hashlib import sha256
import pymongo
from flask import Flask, render_template, request,jsonify, make_response
# from flask_cors import CORS,cross_origin
import requests

app = Flask(__name__)  # initialising the flask app with the name 'app'

class Block:
    def __init__(self,index,previous_hash,current_transction,timestamp,nonce):
        self.index=index
        self.previous_hash = previous_hash
        self.current_transction=current_transction
        self.timestamp=timestamp
        self.nonce=nonce
        self.hash=self.compute_hash()
        #print(self.__dict__)

    def compute_hash(self):
        block_string=json.dumps(self.__dict__,sort_keys=True)
        first_hash=sha256(block_string.encode()).hexdigest()
        second_hash = sha256(first_hash.encode()).hexdigest()
        print(second_hash)
        return second_hash

    def __str__(self):
        return str(self.__dict__)

class BlockChain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.genesis_block()

    def __str__(self):
        return str(self.__dict__)

    def genesis_block(self):
        genesis_block=Block('Genesis',0x0,[3,4,5,6,7],'datetime.now().timestamp()',0)
        genesis_block.hash=genesis_block.compute_hash()
        self.chain.append(genesis_block.hash)
        self.transactions.append(str(genesis_block.__dict__))
        print('Genesis Block is Ready')
        return genesis_block

    def getLastBlock(self):
        return self.chain[-1]

    def proof_of_work(self,block):
        difficulty=1
        block.nonce=0
        computed_hash=block.compute_hash()
        while not(computed_hash.endswith('0'* difficulty) and str(55 * difficulty) in (computed_hash)):
            block.nonce+=1
            computed_hash=block.compute_hash()
        return computed_hash

    def add(self,data):
        block=Block(len(self.chain),self.chain[-1],data,'datetime.now().timestamp()',0)
        block.hash=self.proof_of_work(block)
        print(block.hash)
        self.chain.append(block.hash)
        self.transactions.append(block.__dict__)
        #return json.load(str(block.__dict__).replace('\'','\"'))

    def getTransactions(self,id):
        labels=['Manufacturer','Transportation','Retailer']
        #print(self.transactions)
        while True:
            try:
                if id=='all':
                    for i in range(len(self.transactions)-1):
                        print('{}:\n{}\n'.format(labels[i],self.transactions[i+1]))
                    break
                elif type(id)==int:
                    print(self.transactions[id])
                    break
            except Exception as e:
                print(e)
        return self.transactions
@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/addblocks', methods=['POST'])  # route with allowed methods as POST and GET# route with allowed methods as POST and GET
def main():
    manufacturer={
        'transactions':
            [
                {
                    'timestamp': datetime.now().timestamp(),
                    'product_id': 1,
                    'product_serial': 5000100,
                    'name': 'pant',
                    'from': 'manufacturer x',
                    'to': 'transportation x'
                }

            ]
    }
    transportation = {
        'transactions':
            [
                {
                    'timestamp': datetime.now().timestamp(),
                    'product_id': 1,
                    'product_serial': 5000100,
                    'name': 'pant',
                    'from': 'transportation x',
                    'to': 'retailer x'
                }

            ]
    }
    retailer = {
        'transactions':
            [
                {
                    'timestamp': datetime.now().timestamp(),
                    'product_id': 1,
                    'product_serial': 5000100,
                    'name': 'pant',
                    'from': 'retailer x',
                    'to': 'shelf'
                }

            ]
    }

    B=BlockChain()
    m=B.add(manufacturer)
    t=B.add(transportation)
    r=B.add(retailer)
    trxs = B.getTransactions('all')
    print(trxs)
    return jsonify(trxs[1:])

if __name__ == "__main__":
    #main()
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000

