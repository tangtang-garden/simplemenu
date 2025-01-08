

class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    def printNodes(self):
        tempNode = self.linkList.head
        if tempNode == None:
            print('empty linkList')
            return None
            # raise ValueError('无任何节点')
        while tempNode:
            print(tempNode.title)
            tempNode = tempNode.backward
    def appendNode(self,newNode:Node):
        linkList = self.linkList
        if linkList.head == None:
            linkList.head = newNode
            linkList.tail = newNode
        else:
            linkList.tail.backward = newNode
            linkList.tail = newNode
        linkList.length += 1
        return True
    def popNode(self):
        linkList = self.linkList
        if linkList.length == 0:
            return None
        firstNode = linkList.head
        secondNode = linkList.head
        while firstNode.backward:
            secondNode = firstNode
            firstNode = firstNode.backward
        linkList.tail = secondNode
        linkList.tail.backward = None
        linkList.length -= 1
        if linkList.length == 0:
            linkList.head = None
            linkList.tail = None
        return firstNode
    def appendLeftNode(self,newNode:Node):
        linkList = self.linkList
        if linkList.head == None:
            linkList.head = newNode
            linkList.tail = newNode
        else:
            newNode.backward = linkList.head
            linkList.head = newNode
        linkList.length += 1
        return True
    def popLeftNode(self):
        linkList = self.linkList
        if linkList.length == 0:
            return None
        tempNode = linkList.head
        linkList.head = linkList.head.backward
        tempNode.backward = None
        linkList.length -= 1
        if linkList.length == 0:
            linkList.tail = None
        return tempNode
    def getNode(self,index): # index from 0 ~ length-1
        linkList = self.linkList
        if linkList.head == None:
            return None
        assert 0 <= index <= linkList.length-1,'out of range'
        tempNode = linkList.head
        for _ in range(index):
            tempNode = tempNode.backward
        return tempNode
    def setNode(self,index,value):  # setter value
        tempNode = self.getNode(index)
        if tempNode:
            if type(value) is int:
                value = min(max(0,value),100)
            tempNode.value = value
            return True
        return False
    def clear(self):
        while(self.linkList.length > 0):
            self.popLeftNode()

    