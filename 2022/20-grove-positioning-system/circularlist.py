from node import Node

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

    # get the node that is i nodes away from either head (default), or
    # a node passed as an optional arg.
    def get_node_i(self, i, start_node=None):
        if i > 0 and i > self.length:
            i = i % self.length
        elif i < 0 and i < (0 - self.length):
            i = i % (0 - self.length)
        j = 0
        if start_node == None:
            pos = self.head
        else:
            pos = start_node
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

    def mix(self):
        nodes = self.get_nodes()
        for curr in nodes:
            move_dist = curr.get_val()
            # This node has to swap with the node positioned v places away.
            other = self.get_node_i(move_dist, curr)

            # Swapping involves updating links on up to six nodes:
            # each of the two that are moving, and each of their two
            # neighbours (there may be some overlap)

            a = curr.get_pred()
            b = curr
            c = curr.get_succ()
            e = other.get_pred()
            f = other
            g = other.get_succ()

            a.set_succ(f)
            c.set_pred(f)
            e.set_succ(b)
            g.set_pred(b)
        print("vals: {}".format(self.get_vals()))
        print("nodes: {}".format(self.get_nodes()))


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
