class PagingAlgorithm(object):
    def __init__(self,algoName,numFrames):
        self.algoName = algoName
        self.numFrames = numFrames
        self.numDiskWrites = 0
        self.numPageFaults = 0
        self.numAccesses = 0

        def load(self,address):
            self.numAccesses+=1

        def store(self,address):
            self.numAccesses+=1

        def printSummary(self):
            print("Algorithm: "+str(algoName))
            print("Number of frames: "+str(self.numFrames))
            print("Total memory accesses: "+str(self.numAccesses))
            print("Total page faults: "+str(self.numAccesses))
            print("Total writes to disks: "+str(self.numDiskWrites))


class OptimalAlgorithm(PagingAlgorithm):
    def __init__(self,numFrames):
        PagingAlgorithm.__init__("Optimal",numFrames)




class SecondChanceAlgorithm(PagingAlgorithm):
    def __init__(self, numFrames):
        PagingAlgorithm.__init__("SecondChance", numFrames)