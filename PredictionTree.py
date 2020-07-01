class PredictionTree():
    Item = None                         # 值
    Parent = None                       # 父节点
    Children = None                     # 子节点
    
    def __init__(self,itemValue=None):
        self.Item = itemValue
        self.Children = []
        self.Parent = None
        
    def addChild(self, child):
        newchild = PredictionTree(child) # 添加子节点
        newchild.Parent = self           # 子节点的父节点是当前节点
        self.Children.append(newchild)
        
    def getChild(self, target):
        for chld in self.Children:
            if chld.Item == target:
                return chld
        return None

    def hasChild(self,target):
        found = self.getChild(target)
        if found is not None:
            return True
        else:
            return False
        
    def removeChild(self,child):
        for chld in self.Children:
            if chld.Item==child:
                self.Children.remove(chld)

    def getChildren(self):
        return self.Children
