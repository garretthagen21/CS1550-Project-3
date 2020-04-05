#!/usr/bin/python

import argparse
import sys
from .lru import *
from .optimal import *
from .secondchange import *

def showErrorAndExit(errorReason,errorCode = 1):
    print("[Error] "+errorReason+" Exiting program...\n")
    sys.exit(errorCode)


class MemoryAccess(object):
    def __init__(self,mode,address):
        self.mode = mode
        self.address = address

    def execute(self,pagingAlgorithm):
        if self.mode == 'l':
            pagingAlgorithm.load(self.address)
        elif self.mode == 's':
            pagingAlgorithm.store(self.address)
        else:
            showErrorAndExit("Invalid mode: " + str(self.mode) + " for address: " + self.address)


    # TODO: Get first 20 bits of address
    def parseAddress(self):
        pass
    # TODO: Get last 12 bits of address
    def parseOffset(self):
        pass

class VirtualSimulator(object):
    def __init__(self, traceFile, numFrames, algorithmType):

        # Initialize our trace sequence
        self.memorySequence = []
        tFile = open(traceFile, 'r')
        for line in tFile.readlines():
            lineTokens = line.split()
            memoryAccess = MemoryAccess(lineTokens[0],lineTokens[1])
            self.memorySequence.append(memoryAccess)
        tFile.close()

        # Create paging algorithm
        if algorithmType == "opt":
            self.pagingAlgorithm = OptimalAlgorithm(numFrames)
        elif algorithmType == "lru":
            self.pagingAlgorithm = LRUAlgorithm(numFrames)
        elif algorithmType == "second":
            self.pagingAlgorithm = SecondChanceAlgorithm(numFrames)
        else:
            showErrorAndExit("Invalid algorithm: "+algorithmType)



    def run(self):
        # Execute the memory trace
        for access in self.memorySequence:
            access.execute(self.pagingAlgorithm)

        # Print our summary
        self.pagingAlgorithm.printSummary()



    def loadTraces(self,traceFile):
        traceDict = {}






# ./vmsim –n <numframes> -a <opt|lru|second> <tracefile>

if __name__ == "__main__":

    # Add our program arguments
    parser = argparse.ArgumentParser(description='Virtual memory manager for CS1550')
    parser.add_argument('tracefile', nargs='?', default='empty.txt', type=str,
                        help='The path to the tracefile for the memory accesses')
    parser.add_argument('-n', '--numframes', dest='num_frames', action='store',
                        default=10, type=int,
                        help='The desired number of frames simulate')
    parser.add_argument('-a', '--algorithm', dest='algorithm', action='store',
                        default='opt', type=str,
                        help='The type of algorithm to run. Options: <opt|lru|second>')

    # Parse the arguments
    args = parser.parse_args()

    # Create and run simulator
    virtualSim = VirtualSimulator(args.tracefile, args.num_frames, args.algorithm)
    virtualSim.run()
