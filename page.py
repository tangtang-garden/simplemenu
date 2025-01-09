# dataclass
class Node:
    length = 0
    NULL = const(0)
    PAGE = const(1)
    BOOL = const(2)
    NUM = const(3)
    CHICO = const(4)
    def __init__(self,title,value = 0,incr = 1,nodeType = 0,attr = 0,valueRange=()) -> None:
        self.title = title
        self.backward = None
        self.value = value
        self.incr = incr
        self.nodeType = nodeType    # -
        self.attr = attr
        self.valueRange = valueRange
        Node.length += 1
# dataclass
class Page:
    length = 0
    def __init__(self,title,width=128,height=64) -> None:
        self.title = title
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.linkList = LinkList()
        self.selected = 0
        self.offset = 0
        Page.length += 1
class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0