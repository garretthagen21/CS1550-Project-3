#!/usr/bin/env python3

import argparse
import sys
from algorithms.pagingalgorithm import parseAddressString
from algorithms.lru import LRUAlgorithm
from algorithms.optimal import OptimalAlgorithm
from algorithms.secondchance import SecondChanceAlgorithm


def showErrorAndExit(errorReason,errorCode = 1):
    print("[Error] "+errorReason+" Exiting program...\n")
    sys.exit(errorCode)


class MemoryAccess(object):
    def __init__(self,mode,rawAddr):
        self.mode = mode
        addrTuple = parseAddressString(rawAddr)
        self.address = addrTuple[0]
        self.offset = addrTuple[1]

    def execute(self,pagingAlgorithm):
        if self.mode == 'l':
            pagingAlgorithm.load(self.address)
        elif self.mode == 's':
            pagingAlgorithm.store(self.address)
        else:
            showErrorAndExit("Invalid mode: " + str(self.mode) + " for address: " + self.address)


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
        for memAccess in self.memorySequence:
            self.pagingAlgorithm.access(memAccess.address,memAccess.mode)
            #self.pagingAlgorithm.displayPageTable()

        # Print our summary
        self.pagingAlgorithm.printSummary()

        # Write our csv so we can print graphs
        self.pagingAlgorithm.writeCSV("test_results.csv")






# ./vmsim –n <numframes> -a <opt|lru|second> <tracefile>

if __name__ == "__main__":

    # Add our program arguments
    parser = argparse.ArgumentParser(description='Virtual memory manager for CS1550')
    parser.add_argument('tracefile', nargs='?', default='', type=str,
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
    virtualSim = VirtualSimulator(args.tracefile, int(args.num_frames), args.algorithm)
    virtualSim.run()
