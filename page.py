# dataclass
class Node:
    length = 0
    def __init__(self,title,value = None,attr = 0,valueRange=()) -> None:
        self.title = title
        self.backward = None
        self.value = value
        self.valueRange = valueRange
        self.attr = attr
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