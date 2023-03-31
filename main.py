from block import *
from datacon import *


if __name__ == "__main__": # apparently this is cool
    testMessage = "Hello world!"

    readDatabase()
    #Function testing shenanigans
    testChain = standardChain()
    print(testChain)
    testChain.createStandardBlock(testMessage)
##################

