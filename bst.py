import sys
import random
import copy

class Item(object):
    def __init__(self, key=None, value=None):
        self._key = key
        self._value = value

    def GenRandom(self):
        maxInt = sys.maxint
        self._key = random.randint(0, maxInt)
        self._value = self._key << 2
        return self

    def Key(self):
        return self._key

    def Value(self):
        return self._value

class Node(object):
    def __init__(self, item=None):
        self._item = item
        self._left = None
        self._right = None

    def GetItem(self):
        return self._item

    def SetItem(self, item):
        self._item = item

    def GetLeft(self):
        return self._left

    def SetLeft(self, left):
        self._left = left

    def GetRight(self):
        return self._right

    def SetRight(self, right):
        self._right = right

    def RotateLeft(self):
        p = self.GetRight()
        self.SetRight( p.GetLeft() )
        p.SetLeft( self )
        self = p
        return self

    def RotateRight(self):
        p = self.GetLeft()
        self.SetLeft( p.GetRight() )
        p.SetRight( self )
        self = p
        return self

    def Print(self):
        print( 'node.i=' + str(self.GetItem().Value()) )

class BST(object):
    def __init__(self):
        self._head = Node()

    def Insert(self, item):
        if type(item) is not Item:
            print(type(item))
            return

        h = self._head
        if h.GetItem() is None:
            h.SetItem( item )
            return

        while True:
            hItem = h.GetItem()
            if item.Key() < hItem.Key():
                if h.GetLeft() is None:
                    h.SetLeft( Node( item ) )
                    break
                else:
                    h = h.GetLeft()
            else:
                if h.GetRight() is None:
                    h.SetRight( Node( item ) )
                    break
                else:
                    h = h.GetRight()

    def InsertR(self, parent, node, isLeft, item):
        if node is None:
            if isLeft == True:
                parent.SetLeft( Node( item ) )
            else:
                parent.SetRight( Node( item ) )
            return parent
        elif node.GetItem() is None:
            node.SetItem(item)
            return node

        root = parent == node

        nItem = node.GetItem()
        if item.Key() < nItem.Key():
            self.InsertR( node, node.GetLeft(), True, item )
            n = node.RotateRight()
            if root == False:
                if isLeft == True:
                    parent.SetLeft( n )
                else:
                    parent.SetRight( n )
            return n
        else:
            self.InsertR( node, node.GetRight(), False, item )
            n = node.RotateLeft()
            if root == False:
                if isLeft == True:
                    parent.SetLeft( n )
                else:
                    parent.SetRight( n )
            return n

    def InsertIntoRoot(self, item):
        self._head = self.InsertR(self._head, self._head, None, item)

    def Search(self, key):
        h = self._head
        while True:
            hItem = h.GetItem()
            if hItem is None:
                break
            if key == hItem.Key():
                return hItem
            if key < hItem.Key():
                if h.GetLeft() is not None:
                    h = h.GetLeft()
                else:
                    break
            else:
                if h.GetRight() is not None:
                    h = h.GetRight()
                else:
                    break
        return None

    def JoinLR(self, l, r):
        if r is None:
            return l
        v, n = self.PartitionR(r, r, None, 1)
        n.SetLeft( l )
        return n

    def Remove(self, key):
        parent = h = self._head
        isLeft = None
        f = None
        while True:
            hItem = h.GetItem()
            if hItem is None:
                break
            if key == hItem.Key():
                f = h
                break
            if key < hItem.Key():
                if h.GetLeft() is not None:
                    parent = h
                    isLeft = True
                    h = h.GetLeft()
                else:
                    break
            else:
                if h.GetRight() is not None:
                    parent = h
                    isLeft = False
                    h = h.GetRight()
                else:
                    break
        if f is not None:
            if parent == f:
                self._head = self.JoinLR(f.GetLeft(), f.GetRight())
            else:
                h = self.JoinLR(f.GetLeft(), f.GetRight())
                if isLeft == True:
                    parent.SetLeft( h )
                else:
                    parent.SetRight( h )

    def SelectR(self, node, k):
        tl = 0
        if node.GetLeft() is not None:
            tl, kth = self.SelectR(node.GetLeft(), k)
            if kth is not None:
                return tl, kth

        tl = tl + 1
        if tl == k:
            return tl, node.GetItem()

        tr = 0
        if node.GetRight() is not None:
            tr, kth = self.SelectR(node.GetRight(), k-tl)
            if kth is not None:
                return tr, kth

        return tl + tr, None

    def Select(self, k):
        return self.SelectR(self._head, k)

    def PartitionR(self, parent, node, isLeft, k):
        root = parent == node
        tl = 0
        if node.GetLeft() is not None:
            tl, kth = self.PartitionR(node, node.GetLeft(), True, k)
            if kth is not None:
                n = node.RotateRight()
                if root == False:
                    if isLeft == True:
                        parent.SetLeft( n )
                    else:
                        parent.SetRight( n )
                return tl, kth

        tl = tl + 1
        if tl == k:
            return tl, node

        tr = 0
        if node.GetRight() is not None:
            tr, kth = self.PartitionR(node, node.GetRight(), False, k-tl)
            if kth is not None:
                n = node.RotateLeft()
                if root == False:
                    if isLeft == True:
                        parent.SetLeft( n )
                    else:
                        parent.SetRight( n )
                return tr, kth

        return tl + tr, None

    def Partition(self, k):
        t, n = self.PartitionR(self._head, self._head, None, k)
        if n is not None:
            self._head = n

    def GetLongestPathR(self, node, deep):
        deep = deep + 1
        maxDeep = deep
        if node.GetLeft() is not None:
            maxDeep = max(maxDeep, self.GetLongestPathR(node.GetLeft(), deep))
        if node.GetRight() is not None:
            maxDeep = max(maxDeep, self.GetLongestPathR(node.GetRight(), deep))
        return maxDeep

    def GetLongestPath(self):
        deep = 0
        return self.GetLongestPathR(self._head, deep)

    def InOrder(self, node, visitor):
        if node.GetLeft() is not None:
            self.InOrder(node.GetLeft(), visitor)
        visitor( node.GetItem() )
        if node.GetRight() is not None:
            self.InOrder(node.GetRight(), visitor)

    def Traverse(self, visitor, traverseType):
        if traverseType == 'inorder':
            self.InOrder(self._head, visitor)

    def PrintR(self, indent, node):
        hItem = node.GetItem()
        if hItem is not None:
            print( indent + str( hItem.Value() ) )
        indent += ' '
        if node.GetLeft() is not None:
            self.PrintR(indent, node.GetLeft())
        else:
            print( indent + 'l' )
        if node.GetRight() is not None:
            self.PrintR(indent, node.GetRight())
        else:
            print( indent + 'r' )

    def Print(self):
        self.PrintR('', self._head)
        print( '' )


def PrintVisitor(item):
    print(item.Value())

def TestInsertion(bst, num):
    for i in range(num):
        item = Item().GenRandom()
        #print( 'inserting ' + str(item.Key()) )
        bst.InsertIntoRoot( item )
        #bst.Print()

def Main():
    bst = BST()
    TestInsertion(bst, 10)
    bst.Traverse(PrintVisitor, 'inorder')
    print( bst.GetLongestPath() )
    v,i5 = bst.Select(1)
    bst.Remove(i5.Key())
    #print( i5.Value() )
    bst.Print()

Main()
