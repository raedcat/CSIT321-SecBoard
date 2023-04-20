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
        hash1 = self.ProofOfWork('Genesis', 'Test', 'TBI')

        print('Hash of Genesis: ' + str(hash1[0])) # hash1 is a tuple, hash1[0] gives the hash and hash1[1] gives the nonce value
        print('The above should start with four zeroes')
        print()
        genesis = standardBlock("Genesis", "Test", hash1[1], "TBI") # generate a genesis block when the list (chain) is created
        self.chainList = [] # initiate the list
        self.chainList.append(genesis) # add to the list. append adds to the end of the list. To modify at a certain index, use 'insert(index, object)'
    
    def __str__(self): # print method
        output = ""
        count = 0
        for x in self.chainList:
            count +=1
            output +=("BLOCK {:}\n"
                "Previous Hash:   {:}\n"
                "Data:            {:}\n"
                "Proof of Work:   {:}\n"
                "Correction Hash: {:}\n\n").format(count, x.previousHash, x.data, x.proofOfWork, x.correctionHash)
        return output
# will likely be left as null until correction chain is implemented

    def ProofOfWork(self, previousHash, data, correctionHash): # generates hash and provides nonce value
        nonceValue = -1 # ensures nonce counting will start at 0
        hash1 = ''
        # find nonce value and generate block along with its hash
        while not str(hash1).startswith("0000"): # four zeroes currently chosen as arbitrary difficulty
            nonceValue = nonceValue + 1
            newBlock = json.dumps({
    
                'Previous Hash': previousHash,
                'Data': data,
                'Proof of Work': nonceValue,
                'Correction Hash': correctionHash
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            hash1 = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
            if nonceValue >= 1000000000: # one billion is the limit for nonce searching
                break

        return hash1, nonceValue # returns the completed hash along with the nonce value found as a tuple
            

    def addToChain(self, standardBlock): # add a block to the chain, assuming the block has already been made
        self.chainList.append(standardBlock)
        

    def createStandardBlock(self, data): # create a block by hashing the previous block and finding the proof of work nonce value
        # hash previous block
        previousBlockIndex = len(self.chainList) - 1
        # get the hash of the previous block in the chain
        hashOfPrevious = self.ProofOfWork(self.chainList[previousBlockIndex].previousHash, self.chainList[previousBlockIndex].data, self.chainList[previousBlockIndex].correctionHash)
        # create standardBlock object
        newBlock = standardBlock(hashOfPrevious[0], data, hashOfPrevious[1], self.chainList[previousBlockIndex].correctionHash)
        print(self.chainList[previousBlockIndex].previousHash)
        # add block to the list
        self.chainList.append(newBlock)
        for x in self.chainList:
            print(x.data)
        print('Hash of previous block: ' + hashOfPrevious[0]) #debugging shenanigans
        print()
        return

    def validateChain(self): # ensure the chain list is valid by comparing the hash of the previous block to the stored previous hash

        # first verify the chain starts with the genesis block
        if self.chainList[0].previousHash == 'Genesis':
            print('Genesis found')
        else:
            print('Error validating block: Genesis block not found')
            return 0 # validation fails

        count = -1 # keep track of iterations through loop     
        for x in self.chainList:
            count += 1
            if count == 0:
                continue # skip genesis block
                
            # get previous hash stored in current block
            previous_hash_stored_in_current_block = x.previousHash
            print(previous_hash_stored_in_current_block)

            # hash the previous block
            newBlock = json.dumps({
    
                'Previous Hash': self.chainList[count-1].previousHash,
                'Data': self.chainList[count-1].data,
                'Proof of Work': self.chainList[count-1].proofOfWork,
                'Correction Hash': self.chainList[count-1].correctionHash
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            rehash_previous_block = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
            print(rehash_previous_block)
            
            if previous_hash_stored_in_current_block == rehash_previous_block:
                print('Successfully validated block ' + str(count+1))
            else:
                print('Error validating block ' + str(count+1))
                return 0

            
            
            
