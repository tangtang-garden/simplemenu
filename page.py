# dataclass
class Node:
    length = 0
    def __init__(self,title,value = 0,attr = 0,valueRange=(),valueDesc = None,enable = 0) -> None:
        self.title = title
        self.backward = None
        self.attr = attr
        self.value = value
        self.valueRange = (0,1) if attr == 2 else valueRange
        self.valueDesc = self.value if 
        self.enable = enable
        Node.length += 1
    @property
    def width(self):
        return len(self.title)
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