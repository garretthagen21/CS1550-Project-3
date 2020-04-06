
from pagingalgorithm import *


class PageNode(object):
    def __init__(self, address, refBit = False ,dirtyBit = False, prev=None, next=None):
        self.address = address
        self.refBit = refBit
        self.dirtyBit = dirtyBit
        self.prev = prev
        self.next = next



class SecondChanceAlgorithm(PagingAlgorithm):

    def __init__(self, numFrames, name="SECOND"):
        super().__init__(numFrames, name)
        self.head = None
        self.tail = None
        self.lookupTable = {}

        # Public method

    def access(self, address, mode):

        # Increment accesses
        self.numAccesses += 1

        # Attempt to find the page in memory
        pageNode = self.lookup(address)

        # Page does not exist so we need to load it
        if pageNode is None:

            # Increment page faults
            self.numPageFaults += 1

            # Create new page entry
            pageNode = PageNode(address)

            # If we are full, find a new spot via eviction
            if self.isFull():

                # Iterate through our nodes to find who to remove
                currNode = self.head
                while True:

                    # If the r bit is 1, set it to zero and send it to the back
                    if currNode.refBit:
                        currNode.refBit = False
                        self.remove(currNode)
                        self.append(currNode)
                    else:
                        # Write to disk if dirty bit is 1
                        if currNode.dirtyBit:
                            self.numDiskWrites += 1
                        # Evict this node
                        self.remove(currNode)

                        # Break from the loop
                        break;

                    # If we reached the end, go back to the beginning (simualte, doubly link list)
                    if currNode is self.tail:
                        currNode = self.head
                    else:
                        currNode = currNode.next

            # Insert our new page at the back
            self.append(pageNode)

        # The page already exists in memory so set the reference bit to 1
        else:
            pageNode.refBit = True

        # Only difference between store and load is what we do to the dirty bit
        if mode == "s":
            pageNode.dirtyBit = True

    # Private lookup of page
    def lookup(self, address):
        try:
            return self.lookupTable[address]
        except KeyError:
            return None

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


