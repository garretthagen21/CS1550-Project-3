
from pagingalgorithm import *


class SecondChanceAlgorithm(PagingAlgorithm):

    def __init__(self, numFrames, name="SECOND"):
        super().__init__(numFrames, name)


    def access(self, address, mode):

        # Attempt to find the page in memory
        pageNode = dictLookup(self.lookupTable,address)

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

        # Increment accesses
        self.numAccesses += 1




