
from pagingalgorithm import *


class PageNode(object):
    def __init__(self, address, dirtyBit = False, prev=None, next=None):
        self.address = address
        self.dirtyBit = dirtyBit
        self.prev = prev
        self.next = next



class OptimalAlgorithm(PagingAlgorithm):

    def __init__(self, numFrames, name="OPT",instructionSequence = []):
        super().__init__(numFrames, name)
        self.head = None
        self.tail = None
        self.lookupTable = {}

        # Build the instruction set as a hashtable of instruction:maxLineNum
        self.instructionSet = {}
        for instruction in instructionSequence:
            if not dictLookup(self.instructionSet,instruction.address):
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
            lineDiff = self.findNextAccessDistance(self.instructionSet[currNode.address],self.numAccesses)

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


    def findNextAccessDistance(self,lineNums,thresh):

        # If we are past the maximum instruction, just return (slight optimization)
        maxLine = lineNums[-1]
        if maxLine <= thresh:
            return maxLine - thresh

        # Get the distance between the next instruction and the current one
        for num in lineNums:
            if num > thresh:
                return num - thresh



        # private method to remove page node
    def remove(self, pageNode):

        # Connect prev pointer to next pointer
        if pageNode.prev:
            pageNode.prev.next = pageNode.next

        # Connect next pointer to prev pointer
        if pageNode.next:
            pageNode.next.prev = pageNode.prev

        # If this was the head move it
        if pageNode is self.head:
            self.head = pageNode.next

        # If this was the tail move it
        if pageNode is self.tail:
            self.tail = pageNode.prev

        # Remove entry from hashmap
        del self.lookupTable[pageNode.address]

        # private method to append page node

    def append(self, pageNode):

        # Append to end
        currTail = self.tail
        pageNode.prev = currTail
        if currTail:
            currTail.next = pageNode

        # New tail is page node
        self.tail = pageNode
        self.tail.next = None

        # If this is also the first node we need to set the head
        if not self.head:
            self.head = self.tail

        # Add entry to hashmap lookuptable
        self.lookupTable[pageNode.address] = pageNode

    def isFull(self):
        return len(self.lookupTable) >= self.numFrames

    def displayPageTable(self):
        currNode = self.head
        print("****** Access Num: " + str(self.numAccesses) + " **************")
        print("Linked List: ")

        for i in range(self.numFrames):
            if currNode:
                addr = str(currNode.address)
                bit = str(currNode.refBit)
                currNode = currNode.next
                print("| " + str(i) + " | " + addr + " | " + bit + " |")
            else:
                print("| " + str(i) + " | XXXXXXX | X |")

        print("Lookup Table:")
        i = 0
        for key, value in self.lookupTable.items():
            print("| " + str(i) + " -> " + str(key) + " | " + str(value.refBit) + " |")
            i += 1

        print("\n")


