from block import *
from datacon import *


if __name__ == "__main__": # apparently this is cool
    testMessage = "Hello world!"
    
    x = {"Previous Hash":"Gen", "Data":"10", "Proof of Work": 5,"Correction Hash":"50"}

    #Function testing shenanigans
    testChain = standardChain()
    print(testChain)

    block = testChain.createStandardBlock(testMessage)
    testChain.addToChain(block)

    WriteMainChain(testChain)
##################

