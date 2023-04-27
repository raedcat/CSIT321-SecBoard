import json

def readChain():
    with open('database.json', 'r', encoding='utf-8') as database:
        data = json.load(database)
        return data

def writeBlock(block):
    with open('database.json', 'r+', encoding='utf-8') as database:
        data = json.load(database)
        data["MainChain"].append(block)
        database.seek(0)
        json.dump(data, database, indent=4)

def WriteMainChain(chain):
    
    x = 1
    for i in chain.chainList:
        print(x)
        x +=1
        print(i)
        
    
    #j = json.dumps(data, indent=4)
    
    #print(j)


def writeCorrChain(block):
    print("write correction chain database")