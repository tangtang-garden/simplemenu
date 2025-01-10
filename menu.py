'''simple menu wokwi esp32 oled'''
import time
from page import Page,Node
class Menu:
    '''constant'''
    DO_NOTHING = const(0)
    SWITCH_PAGE = const(1)
    MODIFY_STR = const(2)
    MODIFY_BOOL = const(3)
    MODIFY_NUM_FV = const(4)
    MODIFY_CHOICE_FV = const(5)
    # SWITCH_PAGE_CM = const(6)
    RETURN_PAGE = const(7)
    '''global'''
    display_Buf = []
    page_Table = {}
    FV_num = 0
    def __init__(self) -> None:
        self.keypad = bytearray(16)
    def init(self):
        newPage = self.addPage("main")
        self.appendNode(newPage,Node("[Menu]"))
        self.appendNode(newPage,Node("-Configure",value="configure",nodeType=Desc.PAGE,attr=Menu.SWITCH_PAGE))
        self.appendNode(newPage,Node("-Draw",value = "draw",nodeType=Desc.PAGE,attr=Menu.SWITCH_PAGE))
        self.appendNode(newPage,Node("-Game",value = "game",nodeType=Desc.PAGE,attr=Menu.SWITCH_PAGE))
        self.appendNode(newPage,Node("-other D"))
        self.appendNode(newPage,Node("-other E"))
        self.appendNode(newPage,Node("-other F"))
        self.appendNode(newPage,Node("-other G"))
        self.appendNode(newPage,Node("-About"))
        Menu.display_Buf.append(OptionsPage(newPage))
        newPage = self.addPage("configure")
        self.appendNode(newPage,Node("[Configure]"))
        self.appendNode(newPage,Node("-Name",value="elric",nodeType=Desc.STR,attr=Menu.MODIFY_STR))
        self.appendNode(newPage,Node("-Boolean",nodeType=Desc.BOOL,attr=Menu.MODIFY_BOOL))
        self.appendNode(newPage,Node("-Number",value=50,nodeType=Desc.NUM,attr=Menu.MODIFY_NUM_FV,valueRange=(40,60)))
        self.appendNode(newPage,Node("-Float",value=0.5,nodeType=Desc.NUM,incr=0.1,attr=Menu.MODIFY_NUM_FV,valueRange=(0,1)))
        self.appendNode(newPage,Node("-Choice",value=0,nodeType=Desc.CHOICE,attr=Menu.MODIFY_CHOICE_FV,valueRange=(0,2))) # boundless attention incr = 1 or-1...
        self.appendNode(newPage,Node("-Return",value="main",attr=Menu.RETURN_PAGE))
        newPage = self.addPage("draw")
        self.appendNode(newPage,Node("[Draw]"))
        self.appendNode(newPage,Node("-Return",value="main",attr=Menu.RETURN_PAGE))
        newPage = self.addPage("game")
        self.appendNode(newPage,Node("[Game]"))
        self.appendNode(newPage,Node("-Return",value="main",attr=Menu.RETURN_PAGE))
    def addPage(self,title):
        newPage = Page(title)
        Menu.page_Table[title] = newPage
        return newPage
    def appendNode(self,page:Page,newNode:Node):
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
        Menu.display_Buf[-1].moveUp()
    def moveDown(self):
        Menu.display_Buf[-1].moveDown()
    def click(self):
        Menu.display_Buf[-1].click()
    @classmethod
    def frontViewExit(cls):
        obj = cls.display_Buf.pop()
        cls.FV_num -= 1
        del obj
class OptionsPage:
    def __init__(self,page:Page) -> None:
        self.page = page
        self.node = None # page.linkList.head
        self.desc = Desc()
        self.OP_table={
            Menu.DO_NOTHING:self.OP_null,
            Menu.SWITCH_PAGE:self.OP_switchPage,
            Menu.MODIFY_BOOL:self.OP_modifyBool,
            Menu.MODIFY_NUM_FV:self.OP_modifyNumFV,
            Menu.MODIFY_CHOICE_FV:self.OP_modifyChoiceFV,
            Menu.MODIFY_STR:self.OP_modifyStrKB,
            Menu.RETURN_PAGE:self.OP_returnPage,
        }
    def draw(self,oled):
        tempNode = self.getNode(self.page.offset)
        for i in range(self.page.linkList.length):
            if (i+1)*10 > self.page.height: # list out of range
                break
            nodeDesc = self.desc.nodeDesc(tempNode)
            oled.text(nodeDesc,self.page.x+64+(8-len(nodeDesc))*8,self.page.y+i*10+1) # :>8
            oled.text(tempNode.title ,self.page.x+5,self.page.y+i*10+1)
            if i == self.page.selected:
                oled.rect(self.page.x+2,self.page.y+self.page.selected*10,len(tempNode.title)*9,10)
            tempNode = tempNode.backward
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
        self.node =self.getNode(self.page.offset+self.page.selected)
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
    def OP_returnPage(self):
        self.page = Menu.page_Table.get(self.node.value,self.page)
    def OP_switchPage(self):
        self.page = Menu.page_Table.get(self.node.value,self.page)
        self.page.selected = 1
        self.page.offset = 0
    def OP_modifyBool(self):
        self.node.value =  (self.node.value+1)%2 
    def OP_modifyNumFV(self):
        Menu.display_Buf.append(ModifyNumFV(self.node))
    def OP_modifyChoiceFV(self):
        self.node.value = boundless(self.node.value,self.node.incr,self.node.valueRange)
    def OP_modifyStrKB(self):
        ...
class FV:
    '''use keyPad logic in update'''
    def click(self):
        Menu.frontViewExit()
class ModifyNumFV(FV):
    '''scale > 0.01 '''
    def __init__(self,node:Node) -> None:
        self.node = node
        self.x = 7
        self.y = 16
        self.incr = node.incr # 0.1 if isinstance(self.node.value,float) else 1
        Menu.FV_num += 1        
    def draw(self,oled):
        X = self.x+self.step
        Y = self.y+self.step
        valueRange = self.node.valueRange
        strip = 100*(self.node.value - valueRange[0])//(valueRange[1] - valueRange[0]) # round
        oled.fill_rect(X,Y,114,32,0)
        oled.rect(X,Y,114,32)
        oled.rect(X+5,Y+16,104,8)
        oled.fill_rect(X+5+2,Y+16+2,int(strip),4)
        oled.text(self.node.title[1:8],16+0,24-2) # :>7
        oled.text(str(self.node.value),88,24-2)
    def moveDown(self):
        self.node.value = boundary(self.node.value,self.incr*(-1),self.node.valueRange)
    def moveUp(self):
        self.node.value = boundary(self.node.value,self.incr*1,self.node.valueRange)
    @property
    def step(self):
        return (Menu.FV_num - 1)*2
class Desc:
    NULL = const(0)
    PAGE = const(1)
    BOOL = const(2)
    NUM = const(3)
    CHOICE = const(4)
    STR = const(5)
    def __init__(self) -> None:
        self.node = None
        self.OP_valueDesc={
            Desc.NULL:self.DESC_null,
            Desc.PAGE:self.DESC_page,
            Desc.BOOL:self.DESC_bool,
            Desc.NUM:self.DESC_num,
            Desc.CHOICE:self.DESC_choice,
            Desc.STR:self.DESC_str,
        }
    def nodeDesc(self,node:Node):
        self.node = node
        return self.OP_valueDesc.get(self.node.nodeType)()
    def DESC_null(self):
        return ' '
    def DESC_str(self):
        return self.node.value
    def DESC_page(self):
        return '+'
    def DESC_bool(self):
        return ("OFF","ON")[self.node.value]
    def DESC_num(self):
        return str(self.node.value)
    def DESC_choice(self):
        return ("Small","Middle","Large")[self.node.value]  # [(self.node.value-self.node.valueRange[0])//self.node.incr]
def timed_function(f,*args,**kwargs):
    name = str(f).split(' ')[1]
    def inner_func(*args,**kwargs):
        t = time.ticks_us()
        result = f(*args,**kwargs)
        delta = time.ticks_diff(time.ticks_us(),t)
        print('Function {} Time = {:6.3f}ms'.format(name,delta/1000))
        return result
    return inner_func
def boundary(value, incr, bound:tuple):
    lower_bound = bound[0]
    upper_bound = bound[1]
    return min(upper_bound, max(lower_bound, round(value + incr,2)))    # 0.2+0.1=0.30000001
def boundless(value, incr, bound:tuple):    # incr =1 %(0,10) out: normal
    lower_bound = bound[0]                  # incr =2 %(0,10) out:0,2,4,6,8,10,1,3,5,7,9,0...
    upper_bound = bound[1]
    scope = upper_bound - lower_bound + 1
    value = value + incr
    if value < lower_bound:
        value += scope * ((lower_bound - value) // scope + 1)
    return lower_bound + (value - lower_bound) % scope
def scale(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min