# encoding: utf-8
'''
Date: 2014/12/18

@authors: Songyan Hou/Linyin Wu
'''

class TermNode(object):
    def __init__(self, value): 
    #here the value should be true of false 
        self.index = int(value)
        self.value = value
    def __call__(self, assign):
        return self.value
    def _getNextPos(self, index):
        return self
    def _getNextNeg(self, index):
        return self
    def ITE(self, posNode, negNode):
        if self.value:
            return posNode
        else:
            return negNode
    def printTree(self, visited=set(),  ind=0): 
        print('\t' * ind, self)
    def __eq__(self, other):
        return isinstance(other, TermNode) and self.value == other.value
    def __neq__(self, other):
        return not self.__eq__(other)
    def __repr__(self):
        return "<TerminalNode: %s>" % self.value

class DiagramNode(object):
    def __init__(self, mark, bdd, posNode, negNode):
        self.index = bdd.variable_counter
        bdd.variable_counter += 1
        self.mark = mark
        self.posNode = posNode
        self.negNode = negNode
        self.bdd = bdd
    def __call__(self, assign):
        if assign[self.mark]:
            return self.posNode(assign)
        else:
            return self.negNode(assign)
    def _getNextPos(self, mark):
        if mark == self.mark:
            return self.posNode
        return self
    def _getNextNeg(self, mark):
        if mark == self.mark:
            return self.negNode
        return self
    def ITE(self, posNode, negNode):
        # check if this operation has already been computed before
        compute_key = (self.index, posNode.index, negNode.index)
        if compute_key in self.bdd.computed_table:
            return self.bdd.computed_table[compute_key]
        # Get the smallest variable to split up
        v = min([x for x in [self, posNode, negNode] if isinstance(x, DiagramNode)],
                key=lambda x: x.mark)
        # calculate the positive node
        P = self._getNextPos(v.mark).ITE(posNode._getNextPos(v.mark),
                                           negNode._getNextPos(v.mark))
        # calculate the negative node
        N = self._getNextNeg(v.mark).ITE(posNode._getNextNeg(v.mark),
                                           negNode._getNextNeg(v.mark))
        if P == N: return P
        uniqueNode_key = (v.mark, P.index, N.index)
        if uniqueNode_key in self.bdd.uniqueNode_table:
            R = self.bdd.uniqueNode_table[uniqueNode_key]
        else:
            R = DiagramNode(v.mark, self.bdd, P, N)
            self.bdd.uniqueNode_table[uniqueNode_key] = R
        self.bdd.computed_table[compute_key] = R
        return R
    def printTree(self, visited=set(),  ind=0):
        print('\t' * ind, self)
        self.posNode.printTree(visited, ind + 1)
        self.negNode.printTree(visited, ind + 1)
    def noneGC(self, visited):
    #check the nodes that are in use
        visited.add(self.index)
        for v in (self.posNode, self.negNode):
            if isinstance(v, DiagramNode) and v.index not in visited:
                v.noneGC(visited)
    def __eq__(self, other): 
    #check whether two nodes are the same
        return isinstance(other, DiagramNode) and\
            self.mark == other.mark and\
            self.posNode is other.posNode and\
            self.negNode is other.negNode
    def __neq__(self, other):
        return not self.__eq__(other)
    def __repr__(self):
        return "<DiagramNode: %s>" % (self.mark)


class BinaryDecisionDiagram(object):
    termTrue = TermNode(True)
    termFalse = TermNode(False)
    def __init__(self):
        self.uniqueNode_table = {}
        self.computed_table = {}
        self.variable_counter = 2
        self.last = None
    def newVariable(self, mark):
        uniqueNode_key = (mark, 1, 0)
        if uniqueNode_key in self.uniqueNode_table:
            self.last = self.uniqueNode_table[uniqueNode_key]
            return self.last
        self.last = DiagramNode(mark, self, self.termTrue, self.termFalse)
        self.uniqueNode_table[uniqueNode_key] = self.last
        return self.last
    def apply_not(self, a):
        result = a.ITE(self.termFalse, self.termTrue)
        self.last = result
        return result
    def apply_and(self, a, b):
        result = a.ITE(b, self.termFalse)
        self.last = result
        return result
    def apply_nand(self, a, b):
        result = a.ITE(self.apply_not(b), self.termTrue)
        self.last = result
        return result
    def apply_or(self, a, b):
        result = a.ITE(self.termTrue, b)
        self.last = result
        return result
    def apply_nor(self, a, b):
        result = a.ITE(self.termFalse, self.apply_not(b))
        self.last = result
        return result
    def apply_xor(self, a, b):
        result = a.ITE(self.apply_not(b), b)
        self.last = result
        return result
    def apply_xnor(self, a, b):
        result = a.ITE(b, self.apply_not(b))
        self.last = result
        return result
    def ITE(self, a, b, c):
        result = a.ITE(b,c)
        self.last=result
        return result
    def gc(self, active=[]):
        if self.last is not None:
            visited = set()
            for v in [self.last] + active:
                v.noneGC(visited)
            for key, value in self.uniqueNode_table.items():
                if value.index not in visited:
                    del self.uniqueNode_table[key]