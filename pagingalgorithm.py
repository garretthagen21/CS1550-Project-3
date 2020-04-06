
class PagingAlgorithm(object):

    def __init__(self, numFrames,name = "DEFAULT"):
        self.algoName = name
        self.numFrames = numFrames
        self.numDiskWrites = 0
        self.numPageFaults = 0
        self.numAccesses = 0


    def printSummary(self):
        print("Algorithm: "+str(self.algoName))
        print("Number of frames: "+str(self.numFrames))
        print("Total memory accesses: "+str(self.numAccesses))
        print("Total page faults: "+str(self.numPageFaults))
        print("Total writes to disk: "+str(self.numDiskWrites))

    def writeCSV(self,csvFile):
        pass

    # Pythonic pure virtual functions
    def access(self, address, mode):
        raise NotImplementedError("Error: access() not implemented")
    def displayPageTable(self):
        raise NotImplementedError("Error: showPageTable() not implemented")


# Get the address and offset of the address string in decimal
def parseAddressString(rawAddress):
    hexData = rawAddress.split('x')[1]
    addrPortion = hexData[0:-3]
    offsetPortion = rawAddress[-3:]
    return addrPortion,offsetPortion
