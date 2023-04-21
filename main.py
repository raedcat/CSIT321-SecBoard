from block import *
#from datacon import *


if __name__ == "__main__": # apparently this is cool
    testMessage = "Hello world!"
    testMessage2 = "another message"

    #Function testing shenanigans
    testChain = standardChain()
    print(testChain)
    testChain.createStandardBlock(testMessage)
    print(testChain)
    testChain.createStandardBlock(testMessage2)
    print(testChain)
    testChain.validateChain()
##################

