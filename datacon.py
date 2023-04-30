import json
from block import standardBlock, correctionBlock

def readChain():
    with open('database.json', 'r', encoding='utf-8') as database:
        data = json.load(database)
        return data


def WriteMainChain(chain):
    blocks = []
    for i in chain.chainList:
        if not i:
            print("block doesnt exist")
            blocks.append(None)
        else:
            block = {"Previous Hash":i.previousHash, "Data": i.data, "Proof of work": i.proofOfWork, "Correction hash": i.correctionHash}
            print(block)
            blocks.append(block)
            
    jsonchain = json.dumps({"Main chain":blocks}, indent=4)
    with open("database.JSON", 'w', encoding='utf-8') as data:
        data.write(jsonchain)
        
    


def writeCorrChain(block):
    print("write correction chain database")