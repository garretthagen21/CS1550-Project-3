from pagingalgorithm import *


class OptimalAlgorithm(PagingAlgorithm):

    def __init__(self, numFrames, name="OPT", ):
        super().__init__(numFrames, name)
        self.instructionSet = {}

    # Build the instruction set as a hashtable of instruction:lineNums
    def setInstructions(self, instructionSequence):
        self.instructionSet = {}
        for instruction in instructionSequence:
            if not dictLookup(self.instructionSet, instruction.address):
                self.instructionSet[instruction.address] = [instruction.lineNum]
            else:
                self.instructionSet[instruction.address].append(instruction.lineNum)

    # Public method
    def access(self, address, mode):

        # Attempt to find the page in memory
        pageNode = dictLookup(self.lookupTable, address)

        # Page does not exist so we need to load it
        if pageNode is None:

            # Increment page faults
            self.numPageFaults += 1

            # Create new page entry
            pageNode = PageNode(address)

            # Our page table is full so we need to evict
            if self.isFull():

                # Find node to remove
                nodeToRemove = self.findPageToRemove()

                # Write to disk if dirty bit is 1
                if nodeToRemove.dirtyBit:
                    self.numDiskWrites += 1

                # Evict the node we found
                self.remove(nodeToRemove)

        # The node already exists so remove it, so we can move it to the back
        else:
            self.remove(pageNode)

        # Regardless we will insert the pageNode to the back
        self.append(pageNode)

        # Only difference between store and load is what we do to the dirty bit
        if mode == "s":
            pageNode.dirtyBit = True

        # Increment accesses
        self.numAccesses += 1

    def findPageToRemove(self):

        # Becasue the nodes are sorted in LRU, we want to find the first one that doesnt show up again
        currNode = self.head
        maxDiff = -1
        removalNode = currNode

        while currNode is not None:

            # Find the distance to the next instruction, and filter out instructions weve already seen
            lineDiff, self.instructionSet[currNode.address] = self.findNextAccessDistance(self.instructionSet[currNode.address], self.numAccesses)

            # If the line diff is negative, we should stop now, because it wont show up again and is our lru
            if lineDiff < 0:
                removalNode = currNode
                break

            # Find the node that has the furthest instruction and we will remove that
            elif lineDiff > maxDiff:
                removalNode = currNode
                maxDiff = lineDiff

            # Increment to nextNode
            currNode = currNode.next

        return removalNode

    # This function will return the distance to the closest next instruction
    # And remove all previous instructions, to optimize run time
    def findNextAccessDistance(self, lineNums, thresh):

        # If the list is empty set to -1 else set to actual max
        maxLine = lineNums[-1] if lineNums else -1

        # If we are past the maximum instruction, return negative
        if maxLine <= thresh:
            return (-1, [])

        # Get the distance between the next instruction and the current one
        for index in range(len(lineNums)):
            num = lineNums[index]
            if num > thresh:
                return (num - thresh, lineNums[index:])

