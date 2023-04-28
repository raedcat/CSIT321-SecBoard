from block import *
#from datacon import *


if __name__ == "__main__": # apparently this is cool

    #Function testing shenanigans
    testChain = standardChain()
    testChain.createStandardBlock("Hello world!")
    testChain.createStandardBlock("another message")
    testChain.createStandardBlock('test 3')
    testChain.createStandardBlock('test 4')
    print(testChain)
    testChain.validateChain()
    

    #Election
    testElectionHash = 'test election'

    #Correction Chain
    testChain.createCorrectionBlock('New message!', testElectionHash, 2)
    testChain.createCorrectionBlock('New message 2!', testElectionHash, 5)
    testChain.printCorrectionList()

    #Print chain after corrections
    print("========================")
    print("NEW BLOCKCHAIN")
    print("========================")
    testChain.printTrueList()
##################