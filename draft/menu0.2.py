'''simplemenu wokwi esp32 oled'''
import time
class Menu:
    ''' desc '''
    def __init__(self,oled) -> None:
        self.oled = oled
        self.page = None
        # self.display = Display()
        # self.frontView = View()
        # self.keyboard = Keyboard()
        self.draw_buf = []
        # self.keys_buf = bytearray(16)
    def update(self):
        ...
    def draw(self):
        for page in self.draw_buf:
            page.draw()
    def keypressed(self):
        ...
    def addPage(self,title):
        newPage = Page(title)
        self.page = newPage
        self.current = self.page
        self.pages[title] = self.page
        return newPage
    def removePage(self,title):
        del self.pages[title]
    def OP_NULL(self):
        ...
    def OP_SwitchPage(self):
        ...
    def OP_frontView(self):
        ...
class Keyboard:
    def poll_event(self):
        ...
class View:
    def OP_NULL(self):
        ...
    def OP_frontView(self,oled,node:Node):
        oled.fill_rect(16,24,96,32,0)
        oled.rect(16,24,96,32)
        oled.rect(16+8,40,96-16,8)
        oled.fill_rect(16+8+2,42,round(0.76*node.value),4)
        oled.text(node.title[:6]+' '+'...',16+8,24+8)
class Display:
    def draw(self,oled,page:Page):
        width = page.width
        height = page.height
        nodeX = page.x
        nodeY = page.y
        offset = page.offset
        selected = page.selected
        tempNode = page.getNode(offset)
        for i in range(page.linkList.length):
            if (i+1)*10 > height: # list out of range
                break
            oled.text(tempNode.title,nodeX+10,nodeY+i*10)
            tempNode = tempNode.backward
        oled.fill_rect(nodeX,nodeY+selected*10,7,7)
class Node:
    length = 0
    def __init__(self,title,value = None) -> None:
        self.title = title
        self.backward = None
        self.value = value
        self.nextPag = None
        self.previousPage = None
        Node.length += 1
    def moveUp(self):
        ...
    def moveDown(self):
        ...
    def click(self):
        ...
class Page:
    length = 0
    def __init__(self,title) -> None:
        self.title = title
        self.x = 0
        self.y = 0
        self.width = 128
        self.height = 64
        self.linkList = LinkList()
        self.selected = 0
        self.offset = 0
        Page.length += 1
    def moveUp(self):
        if(self.offset + self.selected <= 0):
            return
        if self.selected <= 0 :
            self.offset -= 1
        else:
            self.selected -= 1
    def moveDown(self):
        if (self.offset + self.selected >= self.linkList.length -1):
            return
        if (self.selected +2)*10 > self.height:
            self.offset += 1
        else:
            self.selected += 1
    def click(self):
        ...
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
class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
def timed_function(f,*args,**kwargs):
    name = str(f).split(' ')[1]
    def inner_func(*args,**kwargs):
        t = time.ticks_us()
        result = f(*args,**kwargs)
        delta = time.ticks_diff(time.ticks_us(),t)
        print('Function {} Time = {:6.3f}ms'.format(name,delta/1000))
        return result
    return inner_func
    