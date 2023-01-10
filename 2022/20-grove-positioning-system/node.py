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
