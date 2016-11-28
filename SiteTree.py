class SiteTree:

    class Node:
        def __init__(self, val, children=[], iFrames=[]):
            self.children = children
            self.iframes = iframes
            self.site = val

        def getVal(self):
            return self.val

        def setVal(self, newVal):
            self.val = newVal

        def getChildren(self):
            return self.children

        def setChildren(self, children):
            self.children = children