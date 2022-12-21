#!/usr/bin/env python3

import sys

class Node:
    def __init__(self, val, pred=None, succ=None):
        self.val = val
        if pred == None:
            self.pred = self
        else:
            self.pred = pred
        if succ == None:
            self.succ = self
        else:
            self.succ = succ

    def __repr__(self):
        pred_str = "None"
        if self.pred != None:
            pred_str = self.pred.get_val()
        succ_str = "None"
        if self.succ != None:
            succ_str = self.succ.get_val()
        return "Node(pred={}, val={}, succ={})".format(pred_str, self.val, succ_str)

    def get_val(self):
        return self.val

    def get_pred(self):
        return self.pred

    def set_pred(self, node):
        self.pred = node

    def get_succ(self):
        return self.succ

    def set_succ(self, node):
        self.succ = node

    # Attaches a new node to the current node by making it the new successor.
    def attach(self, new_node):
        if new_node.pred != new_node or new_node.succ != new_node:
            print("you are in a state of sin")
            exit(0)
        if self.pred == self:
            self.pred = new_node
        new_node.set_pred(self)
        new_node.set_succ(self.succ)
        self.succ.set_pred(new_node)
        self.set_succ(new_node)

    def swap_with_pred(self):
        if self.pred == self:
            print("you are too tired for this, go to sleep")
            exit(0)

        ## Swapping C with B ##
        # A
        self.get_pred().get_pred().set_succ(self)  # 1

        # D
        self.get_succ().set_pred(self.get_pred())  # 6

        # B (pred)
        orig_pred = self.get_pred()
        orig_pred_pred = self.get_pred().get_pred()
        self.get_pred().set_pred(self) # 2
        self.get_pred().set_succ(self.get_succ()) # 3

        # C (self)
        self.set_pred(orig_pred_pred) # 4
        self.set_succ(orig_pred) #5

    def swap_with_succ(self):
        print("GOTHERE: {}".format(self.get_succ().get_val()))
        succ = self.get_succ()
        succ.swap_with_pred()

    def move(self, i):
        print("Moving {}".format(i))
        if i < 0:
            while i < 0:
                self.swap_with_pred()
                i += 1
        elif i > 0:
            while i > 0:
                self.swap_with_succ()
                i -= 1

class CircularList:
    head: Node
    tail: Node
    vals: Node
    length: int
    #orig_vals: [int]	# I want type 'a, not int, oh well.

    # Given a list, constructs a 
    def __init__(self, vals=None):
        self.head = None
        self.tail = None
        self.vals = []
        self.length = 0
        self.orig_vals = vals

        if vals != None and vals != []:
            self.head = Node(vals[0])
            self.length = 1
            self.orig_vals = [v for v in vals]
            self.tail = self.head
            pos = self.head
            for v in vals[1:]:
                pos.attach(Node(v))
                self.length += 1
                pos = pos.get_succ()
            self.tail = pos.get_pred()

    def __repr__(self):
        ok_msg = "idk"
        if self.vals_ok():
            ok_msg = "looks ok, I guess"
        else:
            ok_msg = ">> SOMETHING IS VERY WRONG <<"
        indent = "    "
        nodes = []
        pos = self.head
        while True:
            nodes.append("{}{}{},".format(indent, indent, pos.__repr__()))
            pos = pos.get_succ()
            if pos == self.head:
                break
        nodes_str = "\n".join(nodes)
        return "\n".join([
            "CircularList(",
            "{}head={},".format(indent, self.head),
            "{}tail={},".format(indent, self.tail),
            "{}length={},".format(indent, self.length),
            "{}[".format(indent),
            nodes_str,
            "{}]".format(indent),
            ")",
            "Does this look ok?  {}".format(ok_msg),
        ])

    def get_orig_vals(self):
        return self.orig_vals

    def get_vals(self):
        vals = []
        pos = self.head
        while True:
            vals.append(pos.get_val())
            pos = pos.get_succ()
            if pos == self.head:
                break
        return vals

    def get_nodes(self):
        nodes = []
        pos = self.head
        while True:
            nodes.append(pos)
            pos = pos.get_succ()
            if pos == self.head:
                break
        return nodes

    def get_node_i(self, i):
        if i > 0 and i > self.length:
            i = i % self.length
        elif i < 0 and i < (0 - self.length):
            i = i % (0 - self.length)
        j = 0
        pos = self.head
        while True:
            if j == i:
                return pos
            if i > 0:
                j += 1
            else:
                j -= 1
            pos = pos.get_succ()

    def move(self, x):
        return x

    # This is a very weak check.  False indicates disaster, but True
    # doesn't tell us much.
    def vals_ok(self):
        ordered_vals = self.get_vals()
        if len(self.orig_vals) != len(ordered_vals):
            return False
        for v1,v2 in zip(sorted(self.orig_vals), sorted(ordered_vals)):
            if v1 != v2:
                return False
        return True


def get_numbers(fh):
    return [int(n.rstrip('\n')) for n in fh]


if __name__ == "__main__":
    numbers = get_numbers(sys.stdin)

    clist = CircularList(numbers)

    print(clist.get_vals())
    for n in clist.get_nodes():
        print(n)
    print("-- ")

    for n in numbers:
        clist.move(n)

    print(clist.get_vals())
    for n in clist.get_nodes():
        print(n)
    print("-- ")

    print(clist.get_node_i(3))
    print("-- ")
    print(clist)
