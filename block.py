import hashlib # sha256 shenanigans
import json


class standardBlock: # class to define the standard block, with properties taken from the correctable chain paper
    def __init__(self, previousHash, data, proofOfWork, correctionHash):
        self.previousHash = previousHash # hash of the previous block in the standard chain. The paper describes this as ss ∈ {0,1}^K, which just means it's binary (consists only of 0s and 1s)
        self.data = data # the data of the block, which in our case will for now only be a short text message
        self.proofOfWork = proofOfWork # from the paper: "ctrs represents the prrof of work" which for now I'm assuming is the found nonce value as the paper says it's a natural number (i.e. integers 1, 2, 3, 4... etc)
        self.correctionHash = correctionHash # the hash of the last block in the correction chain, which is required for some reason. Need to look into this

class standardChain: # class defining the standard chain by creating a list of standardBlock objects

    def __init__(self):
        # first initialise nonce value finding
        nonceValue = 0 # this nonce finding method needs to be cleaned up and put into its own function
        newBlock = json.dumps({
    
                'Previous Hash': 'Genesis',
                'Data': 'Test',
                'Proof of Work': nonceValue,
                'Correction Hash': 'TBI' # to be implemented
    
                }, sort_keys=True, indent=4, separators=(',', ': '))
        hash1 = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
        
        # find nonce value and generate block along with its hash
        while not str(hash1).startswith("0000"): # four zeroes currently chosen as arbitrary difficulty
            nonceValue = nonceValue + 1
            newBlock = json.dumps({
    
                'Previous Hash': 'Genesis',
                'Data': 'Test',
                'Proof of Work': nonceValue,
                'Correction Hash': 'TBI'
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            hash1 = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
            if nonceValue >= 1000000000: # one billion is the limit for nonce searching
                break

        print('Hash of Genesis: ' + str(hash1))
        print('The above should start with four zeroes')
        print()
        genesis = standardBlock("Genesis", "Test", nonceValue, "TBI") # generate a genesis block when the list (chain) is created
        self.chainList = [] # initiate the list
        self.chainList.append(genesis) # add to the list. append adds to the end of the list. To modify at a certain index, use 'insert(index, object)'
    
    def __str__(self): # print method
        output = ""
        count = 0
        for x in self.chainList:
            count +=1
            output +=("BLOCK {:}\n"
                "Previous Hash: {:>10}\n"
                "Data: {:>16}\n"
                "Proof of Work: {:>8}\n"
                "Correction Hash: {:>4}\n").format(count, x.previousHash, x.data, x.proofOfWork, x.correctionHash)
            return output
# will likely be left as null until correction chain is implemented

    def addToChain(self, standardBlock): # add a block to the chain, assuming the block has already been made
        self.chainList.append(standardBlock)
        

    def createStandardBlock(self, data): # create a block by hashing the previous block and finding the proof of work nonce value
        # hash previous block
        previousBlockIndex = len(self.chainList) - 1
        # hash the data to be hashed with the block
        hashedData = hashlib.sha256(self.chainList[previousBlockIndex].data.encode('utf-8')).hexdigest()
        
        # In order to hash the block, must convert to json
        nonceValue = 0
        newBlock = json.dumps({
    
                'Previous Hash ': self.chainList[previousBlockIndex].previousHash,
                'Data': hashedData,
                'Proof of Work': nonceValue,
                'Correction Hash': self.chainList[previousBlockIndex].correctionHash
    
                }, sort_keys=True, indent=4, separators=(',', ': '))
        hashOfPrevious = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()

        # find nonce value and generate block along with its hash
        while not str(hashOfPrevious).startswith("0000"): # four zeroes currently chosen as arbitrary difficulty
            nonceValue = nonceValue + 1
            newBlock = json.dumps({
    
                'Previous Hash ': self.chainList[previousBlockIndex].previousHash,
                'Data': hashedData,
                'Proof of Work': nonceValue,
                'Correction Hash': self.chainList[previousBlockIndex].correctionHash
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            hashOfPrevious = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
            if nonceValue >= 1000000000: # one billion is the limit for nonce searching
                break
            
        print('Hashed data: ' + str(hashedData))
        print('Hash of previous block: ' + hashOfPrevious) #debugging shenanigans
        print('This looks different from the genesis hash as we have hashed the Data field')
        return
