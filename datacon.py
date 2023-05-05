import json
import block
import mysql.connector

def databaseConnection():
    return mysql.connector.connect(
        host="103.43.75.136",
        user="secboard",
        password="secboardmysql",
        port="3306",
        database="321DB",
        charset="utf8mb4"
    )

def writeMainBlock():
    #uses the databaseConnection function to establish a connection to the database
    mydb = databaseConnection()
    mycursor = mydb.cursor()

    #creates the MYSQL statement to write the data of the block into the chain
    sql = "INSERT INTO MainChain(PreviousHash, BlockData, ProofofWork, CorrectionHash) Values(%s, %s, %s, %s)"
    values = ()
    
    #executes and commits the insertion of the data
    mycursor.execute(sql, values)
    mydb.commit()

def readMainBlock():
    mydb = databaseConnection()
    mycursor = mydb.cursor()

    sql = "SELECT * FROM MainChain"
    mycursor.execute(sql)

    data = mycursor.fetchall()

    for i in data:
        print(i)

########################################### JSON DATABASE READ WRITE###############################################
###########################################         OBSOLETE       ################################################
#reads the chain from the database
def readChain():
    with open('database.json', 'r', encoding='utf-8') as database:
        data = json.load(database)
        return data

#writes the chains to the database
def WriteMainChain(chain):
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