from block import *
from datacon import *


if __name__ == "__main__": # apparently this is cool
    testMessage = "Hello world!"

    readDatabase()
    x = {"Previous Hash":"Gen", "Data":"10", "Proof of Work": 5,"Correction Hash":"50"}
    writeMainDatabase(x)
    #Function testing shenanigans
    testChain = standardChain()
    print(testChain)
    testChain.createStandardBlock(testMessage)
##################

