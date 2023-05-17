import json
import mysql.connector
from block import *

########################################### MYSQL DATABASE READ WRITE###############################################

def databaseConnection():
    return mysql.connector.connect(
        host="103.43.75.136",
        user="secboard",
        password="secboardmysql",
        port="3306",
        database="321DB",
        charset="utf8mb4"
    )


def writeMainBlock(block):
    #uses the databaseConnection function to establish a connection to the database
    mydb = databaseConnection()
    mycursor = mydb.cursor()

    #creates the MYSQL statement to write the data of the block into the chain
    sql = "INSERT INTO MainChain(PreviousHash, BlockData, ProofofWork, CorrectionHash) Values(%s, %s, %s, %s)"
    values = ()
    
    #executes and commits the insertion of the data
    mycursor.execute(sql, values)
    mydb.commit()
    mydb.close()


def readMainBlock():
    mydb = databaseConnection()
    mycursor = mydb.cursor()

    sql = "SELECT * FROM MainChain"
    mycursor.execute(sql)

    data = mycursor.fetchall()
    mydb.close()
    return data

#to be called when new data is added to the database
#when called it will read the database for the new post then send the data
#to the block.py script to produce a new block, after it will use the
# writeMainChain() method to write the chain to the JSON database
def readNewBlock():
    mydb = databaseConnection()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM posts ORDER BY timestamp DESC LIMIT 1")
    data = mycursor.fetchall()
    mydb.close()
    print("newest post")
    print(data)
    
    #call function to create block from this data

    #call function to Read chain from JSON
    oldChain = readChainJSON()
    print("old chain")
    print(oldChain)

    #add new block to chain
    test = standardChain()
    test.createStandardBlock("testing 132")
    block = test.chainList.pop()
    print(block)

    newChain = appendBlockToChainJSON(block, oldChain)

    print("new chain")
    print(newChain)

    #save chain to JSON
    #WriteMainChain(newChain)

    
########################################### JSON DATABASE READ WRITE###############################################
#reads the chain from the database
def readChainJSON():
    with open('database.json', 'r', encoding='utf-8') as database:
        data = json.load(database)
        return data

def appendBlockToChainJSON(newBlock, oldChain):
    oldChain["Main chain"] += {"Previous Hash":newBlock.previousHash, "Data": newBlock.data, "Proof of work": newBlock.proofOfWork, "Correction hash": newBlock.correctionHash}
    newChain = json.dumps(oldChain, indent=4)
    return newChain
    


#writes the chains to the database
def WriteMainChainJSON(chain):
    blocks = []
    cBlocks = []
    
    #builds all the main chain blocks and adds them to a list
    for i in chain.chainList:
        if not i:
            print("block doesnt exist")
            blocks.append(None)
        else:
            block = {"Previous Hash":i.previousHash, "Data": i.data, "Proof of work": i.proofOfWork, "Correction hash": i.correctionHash}
            print(block)
            blocks.append(block)
    
    #builds all the correction chain blocks and adds them to a list
    for i in chain.correctionList:
        if not i:
            print("block doesnt exist")
            cBlocks.append(None)
        else:
            block = {"Previous hash": i.previousHash, "Data": i.data, "Proof of work": i.proofOfWork, "Election hash": i.electionHash, "Standard head hash": i.standardHeadHash, "Successor hash": i.successorHash}
            print(block)
            cBlocks.append(block)    
            
    #creates the full object with both chains and converts it to json
    jsonchain = json.dumps({"Main chain":blocks, "Correction chain": cBlocks}, indent=4)
    
    #writes the data to the database
    with open("database.JSON", 'w', encoding='utf-8') as data:
        data.write(jsonchain)





if __name__ == "__main__":
    readNewBlock()