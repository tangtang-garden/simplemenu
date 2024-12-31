'''simplemenu wokwi esp32 oled'''
import time
from page import Page,Node
class Menu:
    ''' desc '''
    def __init__(self) -> None:
        self.currentPage = None         # background page
        self.optionsPage = OptionsPage()
        self.modifyPage = ModifyPage()
        self.page_buf = []
        self.pages={}
        self.op={}
        # self.keyboard = Keyboard()
        self.keys_buf = bytearray(16)
    def test(self):
        self.addPage("index")
        self.appendNode(Node("A"))
        self.appendNode(Node("B"))
        self.appendNode(Node("C"))
        self.appendNode(Node("D"))
        self.appendNode(Node("E"))
        self.appendNode(Node("F"))
        self.appendNode(Node("G"))
    def update(self):
        ...
    def draw(self,oled):
        for page in self.page_buf:
            page.draw(oled,self.currentPage)
    # def keypressed(self):
    #     ...
    def addPage(self,title):
        self.currentPage = Page(title)
        self.pages[title] = self.currentPage
        return self.currentPage
    # def removePage(self,title):
    #     # del self.pages[title]
    #     ...

    def moveUp(self):
        self.page_buf[-1].moveUp(self.currentPage)
    def moveDown(self):
        self.page_buf[-1].moveDown(self.currentPage)
    def click(self):
        self.page_buf[-1].click(self.currentPage)
    # @classmethod
    # def creatPage(cls,title):
    #     return Page(title)
    def printNodes(self):
        tempNode = self.currentPage.linkList.head
        if tempNode == None:
            print('empty linkList')
            return None
            # raise ValueError('无任何节点')
        while tempNode:
            print(tempNode.title)
            tempNode = tempNode.backward
    def appendNode(self,newNode:Node):
        linkList = self.currentPage.linkList
        if linkList.head == None:
            linkList.head = newNode
            linkList.tail = newNode
        else:
            linkList.tail.backward = newNode
            linkList.tail = newNode
        linkList.length += 1
        return True
    def popNode(self):
        linkList = self.currentPage.linkList
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
        linkList = self.currentPage.linkList
        if linkList.head == None:
            linkList.head = newNode
            linkList.tail = newNode
        else:
            newNode.backward = linkList.head
            linkList.head = newNode
        linkList.length += 1
        return True
    def popLeftNode(self):
        linkList = self.currentPage.linkList
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
        linkList = self.currentPage.linkList
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
            tempNode.value = value
            return True
        return False
    def clear(self):
        while(self.currentPage.linkList.length > 0):
            self.popLeftNode()    
    def OP_NULL(self):
        ...
    def OP_SwitchPage(self):
        ...
    def OP_frontView(self):
        ...
class Keyboard:
    def poll_event(self):
        ...
class ModifyPage:
    def OP_NULL(self):
        ...
    def OP_frontView(self,oled,node:Node):
        oled.fill_rect(16,24,96,32,0)
        oled.rect(16,24,96,32)
        oled.rect(16+8,40,96-16,8)
        oled.fill_rect(16+8+2,42,round(0.76*node.value),4)
        oled.text(node.title[:6]+' '+'...',16+8,24+8)
class OptionsPage:
    def draw(self,oled,page):
        width = page.width
        height = page.height
        nodeX = page.x
        nodeY = page.y
        offset = page.offset
        selected = page.selected
        tempNode = Menu.getNode(page,offset)
        for i in range(page.linkList.length):
            if (i+1)*10 > height: # list out of range
                break
            oled.text(tempNode.title,nodeX+10,nodeY+i*10)
            tempNode = tempNode.backward
        oled.fill_rect(nodeX,nodeY+selected*10,7,7)
    def moveUp(self,page):
        if(page.offset + page.selected <= 0):
            return
        if page.selected <= 0 :
            page.offset -= 1
        else:
            page.selected -= 1
    def moveDown(self,page):
        if (page.offset + page.selected >= page.linkList.length -1):
            return
        if (page.selected +2)*10 > page.height:
            page.offset += 1
        else:
            page.selected += 1
    def click(self,page):
        ...
def timed_function(f,*args,**kwargs):
    name = str(f).split(' ')[1]
    def inner_func(*args,**kwargs):
        t = time.ticks_us()
        result = f(*args,**kwargs)
        delta = time.ticks_diff(time.ticks_us(),t)
        print('Function {} Time = {:6.3f}ms'.format(name,delta/1000))
        return result
    return inner_func
    