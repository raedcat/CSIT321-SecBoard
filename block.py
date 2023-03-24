class MainBlock:
    def __init__(self, previousHash, message, proof):
        self.previousHash = previousHash
        self.message = message
        self.proof = proof

class CorrectionBlock:
    def __init__(self, previousHash, message, proof):
        self.previousHash = previousHash
        self.message = message
        self.proof = proof