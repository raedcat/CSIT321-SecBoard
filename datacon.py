import json

def readDatabase():
    database = open('database.json')
    data = json.load(database)
    print("test data: {}".format(data))