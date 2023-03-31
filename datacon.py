import json

def readDatabase():
    with open('database.json', 'r', encoding='utf-8') as database:
        data = json.load(database)
        return data

def writeDatabase(Block):
    database = readDatabase()
    with open('database.json', 'w', encoding='utf-8') as database:


