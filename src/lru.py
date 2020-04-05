from .pagingalgorithm import *


class PageNode(object):
    def __init__(self, address, dirtyBit=0, prev=None, next=None):
        self.address = address
        self.dirtyBit = dirtyBit
        self.prev = prev
        self.next = next



class LRUAlgorithm(PagingAlgorithm):

    def __init__(self, numFrames):
        PagingAlgorithm.__init__("LRU", numFrames)
        self.head = None
        self.tail = None
        self.size = 0
        self.lookupTable = {}

    # Override public method
    def load(self, address):

        # Call super method
        super()

        # Attempt to find the page in memory
        pageNode = self.lookupTable[address]

        # Page does not exist so we need to load it
        if pageNode is None:
            # Increment page faults
            self.numPageFaults+=1

            # Create new page entry
            pageNode = PageNode(address)

            # Our page table is full so we need to evict
            if self.isFull():

                # Evict front node if it exists
                tempHead = self.head
                self.remove(tempHead)

                # Write to disk if dirty bit is 1
                if tempHead.dirtyBit == 1:
                    self.numDiskWrites += 1

        # The node already exists so remove it
        else:
            self.remove(pageNode)

        # Regardless we will insert the pageNode to the back
        self.append(pageNode)





    # private method to remove page node
    def remove(self,pageNode):

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
    def append(self,pageNode):

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


