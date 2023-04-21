import json

def readDatabase():
    with open('database.json', 'r', encoding='utf-8') as database:
        data = json.load(database)
        return data

def writeBlock(block):
    with open('database.json', 'r+', encoding='utf-8') as database:
        data = json.load(database)
        data["MainChain"].append(block)
        database.seek(0)
        json.dump(data, database, indent=4)

def WriteChain(chain):
    with open('database.json', 'w', encoding='utf-8') as database:
        json.dump(chain, database, indent=4)


def writeCorrDatabase(block):
    print("write correction chain database")