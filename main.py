from block import *
import hashlib # sha256 shenanigans
import json


if __name__ == "__main__": # apparently this is cool
    testMessage = "Hello world!"

    # Function testing shenanigans
    testChain = standardChain()
    testChain.printChain()
    testChain.createStandardBlock(testMessage)
##################

