'''  '''
import time
class Menu:
    currentPage = None
    def __init__(self,oled):
        self.oled = oled
        self.initMenu()
    def initMenu(self):
        oled = self.oled
        oled.text('     - Backing Recipe -',16,1)
        oled.text('[info] Creat Pages...',16,11)
        indexPage = IndexPage(oled)
        mainPage = FullPage(oled)
        breadPage = FullPage(oled)
        timePage = FullPage(oled)
        setUpPage = FullPage(oled)
        oled.text('[info] Creat Nodes...',16,21)
        indexPage.initPage((Node('Enter'),mainPage))
        mainPage.initPage((Node('[Menu]'),None),(Node('Bread'),breadPage),(Node('Timer'),timePage),(Node('Set Up'),setUpPage))
        breadPage.initPage((Node('[Bread]'),None),(Node('Toast'),None),(Node('Bagel'),None))
        timePage.initPage((Node('[Timer]'),None),(Node('counter'),None))
        setUpPage.initPage((Node('[set Up]'),None),(Node('TestValue',50),EnableNode(oled)),(Node('TestBool',False),None))

        oled.text('[info] finfished...',16,31)
        Menu.currentPage = indexPage
    def display(self):  #update all screen if data is working
        Menu.currentPage.display()
    def moveDown(self):
        Menu.currentPage.moveDown()
    def moveUp(self):
        Menu.currentPage.moveUp()
    def click(self):
        Menu.currentPage.click()
class Page:
    length = 0
    def __init__(self,oled,width = 128,height = 64):
        self.oled = oled
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        Page.length += 1
    def display(self):
        ...
    def moveSelected(self):
        ...
    def moveUp(self):
        ...
    def moveDown(self):
        ...
    def click(self):
        ...
    def longClick(self):
        ...
class IndexPage(Page):
    def __init__(self, oled, width=128, height=64):
        super().__init__(oled, width, height)
        self.selected = 0
        self.offset = 0
        self.linkList = LinkList()
    def initPage(self,*args):   #args is a tuple format is (node,nextpage)
        for node,nextpage in args:
            if nextpage:node.nextPage = nextpage
            self.linkList.appendFromTail(node)
    def display(self):
        height = self.height
        oled = self.oled
        nodeX = self.x
        nodeY = self.y
        offset = self.offset
        selected = self.selected
        tempNode = self.linkList.getNode(offset)
        oled.text(' '+'-BakingRecipe-',nodeX,nodeY)
        oled.text(tempNode.title,16,42)
    def click(self):
        tempNode = self.linkList.getNode(self.offset+self.selected)
        tempNode.click()
    def moveSelected(self,selected):
        self.selected=selected 
        self.oled.fill_rect(self.x+8,self.y+self.selected*10+42,7,7) 
class FullPage(Page):
    def __init__(self,oled,width=128,height=64):
        super().__init__(oled,width,height)
        self.selected = 0
        self.offset = 0
        self.linkList = LinkList()
        self.message = {0:"|"}
        self.initPage()
    def initPage(self,*args): # (node,nextpage)
        linkList = self.linkList
        if args:
            linkList.clear()
            for node,nextpage in args:
                if nextpage:node.nextPage = nextpage
                linkList.appendFromTail(node)
        linkList.appendFromTail(Node('Return'))
    def display(self):
        # self.oled.fill(0) #可局部刷新
        height = self.height
        oled = self.oled
        nodeX = self.x
        nodeY = self.y
        offset = self.offset
        selected = self.selected
        tempNode = self.linkList.getNode(offset)
        for i in range(self.linkList.length):
            if (i+1)*10 > height: # list out of range
                break
            oled.text(tempNode.title,nodeX+10,nodeY+i*10)
            oled.text(tempNode.description,nodeX+100,nodeY+i*10)
            tempNode = tempNode.backward
        self.moveSelected(selected)
        # self.oled.show()
    def moveSelected(self,selected):
        # self.oled.rect(self.x, self.y+self.selected*10, self.width, 10,0) #clear old rect
        self.selected=selected 
        self.oled.fill_rect(self.x+0,self.y+self.selected*10,7,7)    #set new rect
    def moveUp(self):
        if (self.offset + self.selected <= 0):
            return
        if self.selected <= 0 :
            self.offset -=1
        else:
            self.moveSelected(self.selected -1)
        # self.display(self.linkList,self.offset,self.selected)
    def moveDown(self):
        if (self.offset + self.selected >= self.linkList.length -1):
            return
        if (self.selected+2)*10 > self.height:
            self.offset += 1
        else:
            self.moveSelected(self.selected +1)
        # self.display(self.linkList,self.offset,self.selected)
    def click(self):
        tempNode = self.linkList.getNode(self.offset+self.selected)
        tempNode.click()
    def longClick(self):
        ...
    # def setDisplay(self,displayBehavior):
    #     self.displayBehavior = displayBehavior
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
class Node:     # or node class put a var is current page
    length = 0
    def __init__(self,title,value = None):
        self.title = title
        self.value = value
        self.backward = None
        self.nextPage = None
        self.previousPage = None
        self.length += 1
    def click(self):
        nextPage = self.nextPage
        if nextPage:
            previousPage = nextPage.linkList.tail.previousPage
            if previousPage is None:
                nextPage.linkList.tail.previousPage = Menu.currentPage
            Menu.currentPage = nextPage
            return
        if isinstance(self.value,bool):     #consider enable 
            self.value = not self.value
            return
        if self.previousPage:
            Menu.currentPage = self.previousPage
    @property
    def description(self):
        if isinstance(self.value,bool):
            if self.value:
                return 'ON'
            else:
                return "OFF"
        if isinstance(self.value,(int,float)):
            return str(self.value)
        return ""
class EnableNode(Page): # node set value enable 
    def __init__(self,oled,width=96,height=32):
        super().__init__(oled,width,height)
        self.tempNode = None
        self.backPage = None
        self.linkList=LinkList()
        self.initPage()
    def initPage(self): # nodes here
        self.linkList.appendFromTail(Node('Return'))
    def display(self):
        oled = self.oled
        self.catchNode()
        if self.backPage is None:
            self.backPage = self.linkList.tail.previousPage
        self.backPage.display()
        oled.fill_rect(16,24,self.width,self.height,0)
        oled.rect(16,24,self.width,self.height)
        oled.rect(16+8,40,96-16,8)
        oled.fill_rect(16+8+2,42,round(0.76*self.tempNode.value),4)
        oled.text(self.tempNode.title[:6]+' '+self.tempNode.description,16+8,24+8)
    def moveUp(self):
        if type(self.tempNode.value) is int:
            self.tempNode.value = min(max(0,self.tempNode.value +1 ),100)
    def moveDown(self):
        if type(self.tempNode.value) is int:
            self.tempNode.value = min(max(0,self.tempNode.value -1 ),100)
    def click(self):
        self.linkList.tail.click()
    def catchNode(self):
        if self.tempNode is None:
            tempPage = self.linkList.tail.previousPage
            self.tempNode = tempPage.linkList.getNode(tempPage.offset+tempPage.selected)
class Task:
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
# class DisplayBehavior:  # (metaclass = ABCmeta)
#   # @abstractclassmethod
#   def display(self):
#       ...

# class MenuDisplayVertically(DisplayBehavior):
#   def display(self):
#       ...
''' -End- '''