
from pagingalgorithm import *


class PageNode(object):
    def __init__(self, address, dirtyBit = 0, prev = None, next = None):
        self.address = address
        self.dirtyBit = dirtyBit
        self.prev = prev
        self.next = next



class LRUAlgorithm(PagingAlgorithm):

    def __init__(self, numFrames, name = "LRU"):
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

            # Our page table is full so we need to evict
            if self.isFull():

                # Write to disk if dirty bit is 1
                if self.head.dirtyBit == 1:
                    self.numDiskWrites += 1

                # Evict front node if it exists
                self.remove(self.head)

        # The node already exists so remove it, so we can move it to the back
        else:
            self.remove(pageNode)

        # Regardless we will insert the pageNode to the back
        self.append(pageNode)

        # Only difference between store and load is what we do to the dirty bit
        if mode == "s":
            pageNode.dirtyBit = 1


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


    def displayPageTable(self):
        currNode = self.head
        print("****** Access Num: "+str(self.numAccesses)+" **************")
        print("Linked List: ")

        for i in range(self.numFrames):
            if currNode:
                addr = str(currNode.address)
                bit = str(currNode.dirtyBit)
                currNode = currNode.next
                print("| "+str(i)+" | "+addr+" | "+bit+" |")
            else:
                print("| " + str(i) + " | XXXXXXX | X |")

        print("Lookup Table:")
        i = 0
        for key,value in self.lookupTable.items():
            print("| "+str(i)+" -> "+str(key)+" | "+str(value.dirtyBit)+" |")
            i+=1

        print("\n")