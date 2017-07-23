#!/usr/bin/python3


p = None
mass = []

class Node:
    def __init__(self, value):
        self.r = None
        self.l = None
        self.v = value


class Tree():
    def __init__(self):
        self.root = None

    def getroot(self):
        return self.root

    def add(self, value):
        if self.root == None:
            self.root = Node(value)
        else:
            self._add(value, self.root)

    def _add(self, value, node):
        global p
        if value == 0 and node.v != 0:
            if node.l == None:
                node.l = Node(value)
                p = node
            elif node.r == None:
                node.r = Node(value)
                p = node
        elif value == 0 and node.v == 0:
            self._add(value, p)
        else:
            if node.l == None:
                node.l = Node(value)
                p = node.l
            elif node.r == None:
                node.r = Node(value)
                p = node.r

    def find(self, value):
        if self.root != None:
            return self._find(value, self.root)
        else:
            return None

    def _find(self, value, node):
        if value == node.v:
            return node
        elif value < node.v and node.l != None:
            self._find(value, node.l)
        elif value > node.v and node.r != None:
            self._find(value, node.r)

    def delete_tree(self):
        self.root = None

    def printTree(self):
        if self.root != None:
            self._printTree(self.root)

    def _printTree(self, node):
        if node != None:
            self._printTree(node.l)
            mass.append(node.v)

    
def tree_build(mass):
    global p
    tree = Tree()
    tree.root = Node(mass[0])
    p = tree.root
    for i in range(1, len(mass)):
        if mass[i] != 0:
            tree._add(mass[i], p)
    tree.printTree()
    print(tree.find(10))


def main():
    with open('input_10a.txt', 'r') as file:
        mass = file.readline().split()
    tree_build(mass)




if __name__ == "__main__":
    main()