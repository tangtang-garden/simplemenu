'''simplemenu wokwi esp32 oled'''
import time
from collections import deque
class Menu:
    def __init__(self) -> None:
        self.page = Page(Node("No DATA"))
        self.currentPage = self.Page
        # self.display = DisplayOled()
        self.keyboard = Keyboard()
        self.keys_buf = bytearray(8)
    def display(self):
        self.currentPage.display()
    def moveDown(self):
        self.currentPage.display()
    def moveUp(self):
        self.currentPage.moveUp()
    def click(self):
        self.currentPage.click()
    def longClick(self):
        ...
class Keyboard:
    def poll_event(self):
        ...

class Page:
    length = 0
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.width = 128
        self.heigth = 64
        self.linkList = deque()
        self.selected = 0
        self.offset = 0
        Page.length += 1
    def appendNode(self,title,value=None):
        newNode = Node(title,value)
        self.linkList.append(newNode)
    def appendLeftNode(self,title,value=None):
        newNode = Node(title,value)
        self.linkList.appendleft(newNode)
    def clearNode(self):
        self.linkList.clear()
    def indexNode(self,node):
        return self.linkList.index(node)
    def insertNode(self,index,newnode):
        self.linkList.insert(index,newnode)
    def popNode(self):
        node = self.linkList.pop()
        return node
    def popLeftNode(self):
        node = self.linkList.popleft()
        return node
    def removeNode(self,node):
        self.linkList.remove(node)
    def reverseNode(self):
        self.linkList.reverse()
    def rotate(self,n=1):
        self.linkList.rotate(n)
    def printNode(self):
        if len(self.linkList) < 1:
            print('empty linkList')
            return
        for node in self.linkList:
            print(node.title,end='|')
        else:
            print(f'linkLink length :{len(self.linkList)}')
class Node:
    length = 0
    def __init__(self,title,value = None) -> None:
        self.title = title
        self.value = value
        self.nextPag = None
        self.previousPage = None
        Node.length += 1
class DisplayOled:
    ...

class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    def printLinkList(self):
        tempNode = self.head
        if tempNode == None:
            print('empty linkList')
            return None
            # raise ValueError('无任何节点')
        while tempNode:
            print(tempNode.title)
            tempNode = tempNode.backward
    def appendFromTail(self,newNode:Node):
        if self.head == None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.backward = newNode
            self.tail = newNode
        self.length += 1
        return True
    def popTail(self):
        if self.length == 0:
            return None
        firstNode = self.head
        secondNode = self.head
        while firstNode.backward:
            secondNode = firstNode
            firstNode = firstNode.backward
        self.tail = secondNode
        self.tail.backward = None
        self.length -= 1
        if self.length == 0:
            self.head = None
            self.tail = None
        return firstNode
    def appendFromHead(self,newNode:Node):
        if self.head == None:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.backward = self.head
            self.head = newNode
        self.length += 1
        return True
    def popHead(self):
        if self.length == 0:
            return None
        tempNode = self.head
        self.head = self.head.backward
        tempNode.backward = None
        self.length -= 1
        if self.length == 0:
            self.tail = None
        return tempNode
    def getNode(self,index): # index from 0 ~ length-1
        if self.head == None:
            return None
        assert 0 <= index <= self.length-1,'out of range'
        tempNode = self.head
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
        while(self.length > 0):
            self.popHead()
def timed_function(f,*args,**kwargs):
    name = str(f).split(' ')[1]
    def inner_func(*args,**kwargs):
        t = time.ticks_us()
        result = f(*args,**kwargs)
        delta = time.ticks_diff(time.ticks_us(),t)
        print('Function {} Time = {:6.3f}ms'.format(name,delta/1000))
        return result
    return inner_func
    