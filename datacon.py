import json

def readDatabase():
    with open('database.json', 'r', encoding='utf-8') as database:
        data = json.load(database)
        return data

def writeMainDatabase(block):
    with open('database.json', 'r+', encoding='utf-8') as database:
        data = json.load(database)
        data["MainChain"].append(block)
        database.seek(0)
        json.dump(data, database, indent=4)


def writeCorrDatabase(block):
    print("write corr database")