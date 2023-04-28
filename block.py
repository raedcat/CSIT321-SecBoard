import hashlib # sha256 shenanigans
import json


class standardBlock: # class to define the standard block, with properties taken from the correctable chain paper
    def __init__(self, previousHash, data, proofOfWork, correctionHash):
        self.previousHash = previousHash # hash of the previous block in the standard chain. The paper describes this as ss ∈ {0,1}^K, which just means it's binary (consists only of 0s and 1s)
        self.data = data # the data of the block, which in our case will for now only be a short text message
        self.proofOfWork = proofOfWork # from the paper: "ctrs represents the prrof of work" which for now I'm assuming is the found nonce value as the paper says it's a natural number (i.e. integers 1, 2, 3, 4... etc)
        self.correctionHash = correctionHash # the hash of the last block in the correction chain, to be used for validating the chain in case a correction exists

class correctionBlock: # class to define the standard block, with properties taken from the correctable chain paper
    def __init__(self, previousHash, data, proofOfWork, electionHash, successorHash, standardHeadHash):
        self.previousHash = previousHash 
        self.data = data # the new data to correct the previous, whether it is a new message or null
        self.proofOfWork = proofOfWork
        self.electionHash = electionHash # hash of election TX E
        self.successorHash = successorHash # hash of successor of the block to be corrected BSi, i.e. H(BSi+1)
        self.standardHeadHash = standardHeadHash # hash value of the head of the standard chain

class standardChain: # class defining the standard chain by creating a list of standardBlock objects

    def __init__(self):
        hash1 = self.ProofOfWork('Genesis', 'Test', 'Correction')

        print('Hash of Genesis: ' + str(hash1[0])) # hash1 is a tuple, hash1[0] gives the hash and hash1[1] gives the nonce value
        print('The above should start with four zeroes')
        print()
        genesis = standardBlock("Genesis", "Test", hash1[1], "Correction") # generate a genesis block when the list (chain) is created
        self.chainList = [] # initiate the list
        self.chainList.append(genesis) # add to the list. append adds to the end of the list. To modify at a certain index, use 'insert(index, object)'

        # create correction chain
        self.correctionList = []
        # for correctionChain, refer to first object in chainList, as the genesis is shared between both and the correctionList needs to consist of correctionBlock objects
    
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

    def printCorrectionList(self):
        output = ""
        count = 0
        for x in self.correctionList:
            count +=1
            output +=("\nCORRECTION BLOCK {:}\n"
                "Previous Hash:   {:}\n"
                "Data:            {:}\n"
                "Proof of Work:   {:}\n"
                "Election Hash:   {:}\n"
                "Successor Hash:  {:}\n"
                "Head Hash:       {:}\n").format(count, x.previousHash, x.data, x.proofOfWork, x.electionHash, x.successorHash, x.standardHeadHash)
        print(output)

    def printTrueList(self):
        output = ""
        count = 0
        corrections = 0
        for x in self.chainList:
            count +=1
            if x == '':
                output +=("CORRECTION BLOCK {:}\n"
                "Previous Hash:   {:}\n"
                "Data:            {:}\n"
                "Proof of Work:   {:}\n"
                "Election Hash:   {:}\n"
                "Successor Hash:  {:}\n"
                "Head Hash:       {:}\n\n").format(count, self.correctionList[corrections].previousHash, self.correctionList[corrections].data, self.correctionList[corrections].proofOfWork, self.correctionList[corrections].electionHash, self.correctionList[corrections].successorHash, self.correctionList[corrections].standardHeadHash)
                corrections += 1
            else:
                output +=("BLOCK {:}\n"
                    "Previous Hash:   {:}\n"
                    "Data:            {:}\n"
                    "Proof of Work:   {:}\n"
                    "Correction Hash: {:}\n\n").format(count, x.previousHash, x.data, x.proofOfWork, x.correctionHash)
        print(output)                

    def ProofOfWork(self, previousHash, data, correctionHash): # generates hash and provides nonce value
        nonceValue = -1 # ensures nonce counting will start at 0
        hash1 = ''
        # find nonce value and generate block along with its hash
        while not str(hash1).startswith("0000"): # four zeroes currently chosen as arbitrary difficulty
            nonceValue = nonceValue + 1
            newBlock = json.dumps({
    
                'Previous Hash': previousHash,
                'Data': hashlib.sha256(data.encode('utf-8')).hexdigest(), # hash data according to paper G(xs)
                'Proof of Work': nonceValue,
                'Correction Hash': correctionHash
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            hash1 = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
            if nonceValue >= 1000000000: # one billion is the limit for nonce searching
                break
        return hash1, nonceValue # returns the completed hash along with the nonce value found as a tuple

    def ProofOfWorkCorrection(self, previousHash, data, electionHash, successorHash, headHash): # generates hash and provides nonce value
        nonceValue = -1 # ensures nonce counting will start at 0
        hash1 = ''
        # find nonce value and generate block along with its hash
        while not str(hash1).startswith("0000"): # four zeroes currently chosen as arbitrary difficulty
            nonceValue = nonceValue + 1
            newBlock = json.dumps({
    
                'Previous Hash': previousHash,
                'Data': hashlib.sha256(data.encode('utf-8')).hexdigest(), # hash data according to paper G(xs)
                'Proof of Work': nonceValue,
                'Election Hash': electionHash,
                'Successor Hash': successorHash,
                'Standard Head Hash': headHash
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            hash1 = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
            if nonceValue >= 1000000000: # one billion is the limit for nonce searching
                break
        return hash1, nonceValue # returns the completed hash along with the nonce value found as a tuple
            
        

    def createStandardBlock(self, data): # create a block by hashing the previous block and finding the proof of work nonce value
        # get previous block index
        previousBlockIndex = len(self.chainList) - 1
        # get the hash of the previous block in the chain
        hashOfPrevious = self.ProofOfWork(self.chainList[previousBlockIndex].previousHash, self.chainList[previousBlockIndex].data, self.chainList[previousBlockIndex].correctionHash)
        # find nonce of new block
        newNonce = self.ProofOfWork(hashOfPrevious[0], data, self.chainList[previousBlockIndex].correctionHash)
        # create standardBlock object
        newBlock = standardBlock(hashOfPrevious[0], data, newNonce[1], self.chainList[previousBlockIndex].correctionHash)
        # add block to the list
        self.chainList.append(newBlock)
        return

    def createCorrectionBlock(self, data, electionHash, block_replace_number): # this occurs after a successful election to correct a block
        if not self.correctionList: # nothing has been added to the correction chain and thus data must be taken from the genesis of the standard chain
            # get the hash of the genesis block
            newBlock = json.dumps({
    
                'Previous Hash': self.chainList[0].previousHash,
                'Data': hashlib.sha256((self.chainList[0].data).encode('utf-8')).hexdigest(),
                'Proof of Work': self.chainList[0].proofOfWork,
                'Correction Hash': self.chainList[0].correctionHash
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            hashOfPrevious = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()

            # get hash of election

            # get hash of successor hash

            # get hash of head of standard chain
            headBlock = json.dumps({
    
                'Previous Hash': self.chainList[-1].previousHash, # [-1] gets the last element in the list
                'Data': hashlib.sha256((self.chainList[-1].data).encode('utf-8')).hexdigest(),
                'Proof of Work': self.chainList[-1].proofOfWork,
                'Correction Hash': self.chainList[-1].correctionHash
    
            }, sort_keys=True, indent=4, separators=(',', ': '))
            headHash = hashlib.sha256(headBlock.encode('utf-8')).hexdigest()


            # find nonce of new block
            newNonce = self.ProofOfWorkCorrection(hashOfPrevious, data, 'Election Hash TBI', 'Successor Hash TBI', headHash)

            # create correctionBlock object
            newBlock = correctionBlock(hashOfPrevious, data, newNonce[1], 'Election Hash TBI', 'Successor Hash TBI', headHash)

            # add the block to the correction list
            self.correctionList.append(newBlock)

            # delete the data of the block being replaced
            self.chainList[block_replace_number - 1] = ''

            return

            
            
        # if the correction list is not empty, proceed as normal
        # get previous block index
        previousBlockIndex = len(self.correctionList) - 1
        # get the hash of the previous correction block
        newBlock = json.dumps({
    
            'Previous Hash': self.correctionList[previousBlockIndex].previousHash,
            'Data': hashlib.sha256((self.correctionList[previousBlockIndex].data).encode('utf-8')).hexdigest(),
            'Proof of Work': self.correctionList[previousBlockIndex].proofOfWork,
            'Election Hash': self.correctionList[previousBlockIndex].electionHash,
            'Successor Hash': self.correctionList[previousBlockIndex].successorHash,
            'Standard Head Hash': self.correctionList[previousBlockIndex].standardHeadHash

        }, sort_keys=True, indent=4, separators=(',', ': '))
        hashOfPrevious = hashlib.sha256(newBlock.encode('utf-8')).hexdigest()
        
        # get hash of election
        
        # get hash of successor hash

        # get hash of head of standard chain
        headBlock = json.dumps({
    
            'Previous Hash': self.chainList[-1].previousHash, # [-1] gets the last element in the list
            'Data': hashlib.sha256((self.chainList[-1].data).encode('utf-8')).hexdigest(),
            'Proof of Work': self.chainList[-1].proofOfWork,
            'Correction Hash': self.chainList[-1].correctionHash
    
        }, sort_keys=True, indent=4, separators=(',', ': '))
        headHash = hashlib.sha256(headBlock.encode('utf-8')).hexdigest()

        # find nonce of new block
        newNonce = self.ProofOfWorkCorrection(hashOfPrevious, data, 'Election Hash', 'Successor Hash', 'Head Hash')

        # create correctionBlock object
        newBlock = correctionBlock(hashOfPrevious, data, newNonce[1], 'Election Hash TBI', 'Successor Hash TBI', headHash)

        # add the block to the correction list
        self.correctionList.append(newBlock)

        # delete the data of the block being replaced
        self.chainList[block_replace_number - 1] = ''

    def validateChain(self): # ensure the chain list is valid by comparing the hash of the previous block to the stored previous hash

        # first verify the chain starts with the genesis block
        if self.chainList[0].previousHash == 'Genesis':
            print('Genesis found, which is block 1')
        else:
            print('Error validating block: Genesis block not found')
            return 0 # validation fails

        count = -1 # keep track of iterations through loop
        corrections = 0 # keep track of how many corrected blocks have been found, to ensure it matches the amount of correction blocks in the correction chain
        for x in self.chainList:
            count += 1
            if count == 0:
                continue # skip genesis block

            # if null, a correction has occurred. Skip this block, and the next
            if self.chainList[count] == '':
                corrections += 1
                continue # correction block is validated by validating the corresponding election, which is TBI

            if self.chainList[count-1] == '':
                continue 
                
            # get previous hash stored in current block
            previous_hash_stored_in_current_block = x.previousHash
            print(previous_hash_stored_in_current_block)

            # hash the previous block
            newBlock = json.dumps({
    
                'Previous Hash': self.chainList[count-1].previousHash,
                'Data': hashlib.sha256((self.chainList[count-1].data).encode('utf-8')).hexdigest(),
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

        if corrections != len(self.correctionList):
            return 0
        else:
            return 1

            
            
            
