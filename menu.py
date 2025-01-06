'''simple menu wokwi esp32 oled'''
import time
from page import Page,Node
class Menu:
    '''constant'''
    DO_NOTHING = const(0)
    SWITCH_PAGE = const(1)
    MODIFY_BOOL = const(2)
    FRONTVIEW_MODIFY_NUM = const(3)
    '''global'''
    display_Buf = []
    page_Table = {}
    front_View_Length = 0
    def __init__(self) -> None:
        self.keypad = bytearray(16)
    def init(self):
        newPage = self.addPage("index")
        self.appendNode(newPage,Node("About",value="about",attr=Menu.SWITCH_PAGE))
        self.appendNode(newPage,Node("Configure"))
        self.appendNode(newPage,Node("Game"))
        self.appendNode(newPage,Node("other D"))
        self.appendNode(newPage,Node("other E"))
        self.appendNode(newPage,Node("other F"))
        self.appendNode(newPage,Node("other G"))
        Menu.display_Buf.append(OptionsPage(newPage))
        newPage = self.addPage("about")
        self.appendNode(newPage,Node("bool",value = 0,attr=Menu.MODIFY_BOOL))
        self.appendNode(newPage,Node("value",value=50,attr=Menu.FRONTVIEW_MODIFY_NUM,valueRange=(40,60)))
        self.appendNode(newPage,Node("about 1"))
        self.appendNode(newPage,Node("about 1"))
        self.appendNode(newPage,Node("return"))
    def addPage(self,title):
        newPage = Page(title)
        Menu.page_Table[title] = newPage
        return newPage
    def appendNode(page:Page,newNode:Node):
        linkList = page.linkList
        if linkList.head == None:
            linkList.head = newNode
            linkList.tail = newNode
        else:
            linkList.tail.backward = newNode
            linkList.tail = newNode
        linkList.length += 1
        # return True     
    def update(self):
        ...
    def draw(self,oled):
        for item in Menu.display_Buf:
            item.draw(oled)
    def moveUp(self):
        ...
    def moveDown(self):
        ...
    def click(self):
        ...
class OptionsPage:
    def __init__(self,page:Page) -> None:
        self.page = page
        self.node = None
        self.OP_table={
            0x0:self.OP_null,
            0x1:self.OP_switchPage,
            0x2:self.OP_modifyBool,
            0x3:self.OP_frontViewModifyNum,
        }
    def draw(self,oled):
        tempNode = self.getNode(self.page.offset)
        for i in range(self.page.linkList.length):
            if (i+1)*10 > self.page.height: # list out of range
                break
            oled.text(tempNode.title,self.page.x+10,self.page.y+i*10)
            tempNode = tempNode.backward
        oled.fill_rect(self.page.x,self.page.y+self.page.selected*10,7,7)
    def moveUp(self):
        if(self.page.offset + self.page.selected <= 0):
            return
        if self.page.selected <= 0 :
            self.page.offset -= 1
        else:
            self.page.selected -= 1
    def moveDown(self):
        if (self.page.offset + self.page.selected >= self.page.linkList.length -1):
            return
        if (self.page.selected +2)*10 > self.page.height:
            self.page.offset += 1
        else:
            self.page.selected += 1
    def click(self):
        index = self.page.offset+self.page.selected
        self.node = self.getNode(index)
        self.OP_table.get(self.node.attr)()
    def getNode(self,index): # index from 0 ~ length-1
        linkList = self.page.linkList
        if linkList.head == None:
            return None
        assert 0 <= index <= linkList.length-1,'out of range'
        tempNode = linkList.head
        for _ in range(index):
            tempNode = tempNode.backward
        return tempNode
    def OP_null(self):
        pass
    def OP_switchPage(self):
        self.page = Menu.page_Table.get(self.node.value)
    def OP_modifyBool(self):
        self.node.value = not self.node.value
    def OP_frontViewModifyNum(self):
        Menu.display_Buf.append(FrontViewModifyNum(self.node))
class FrontViewModifyNum:
    def __init__(self,node:Node) -> None:
        self.node = node
        self.x = 7
        self.y = 16
        Menu.front_View_Length += 1        
    def draw(self,oled):
        X = self.x+self.step
        Y = self.y+self.step
        valueRange = self.node.valueRange
        strip = 100//(valueRange[1] - valueRange[0])*(self.node.value - valueRange[0])
        oled.fill_rect(X,Y,114,32,0)
        oled.rect(X,Y,114,32)
        oled.rect(X+5,Y+16,104,8)
        oled.fill_rect(X+5+2,Y+16+2,strip,4)
        oled.text(self.node.title[:5]+f"{self.node.value:>7}",16+8,24+8)
    def moveDown(self):
        ...
    def moveUp(self):
        ...
    def click(self):
        ...
    @property
    def step(self):
        return (Menu.front_View_Length - 1)*2 
def timed_function(f,*args,**kwargs):
    name = str(f).split(' ')[1]
    def inner_func(*args,**kwargs):
        t = time.ticks_us()
        result = f(*args,**kwargs)
        delta = time.ticks_diff(time.ticks_us(),t)
        print('Function {} Time = {:6.3f}ms'.format(name,delta/1000))
        return result
    return inner_func
def boundary(value, incr, lower_bound, upper_bound):
    return min(upper_bound, max(lower_bound, value + incr))
def boundless(value, incr, lower_bound, upper_bound):
    scope = upper_bound - lower_bound + 1
    value = value + incr
    if value < lower_bound:
        value += scope * ((lower_bound - value) // scope + 1)
    return lower_bound + (value - lower_bound) % scope