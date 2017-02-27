#!/usr/bin/python3

class NodeState(object):

    def __init__(self, parent, *args):
        self.parent = parent
        if len(args) == 6:
            self.left = [args[0], args[1], args[2]]
            self.right = [args[3], args[4], args[5]]
        elif len(args) == 1:
            try:
                f = open(args[0], 'r')
                self.left = [int(x) for x in list(f.readline()[:-1].split(','))]
                self.right = [int(x) for x in list(f.readline()[:-1].split(','))]
            except:
                raise ValueError
        else:
            raise ValueError
        self.max_m = self.left[0] + self.right[0]
        self.max_c = self.left[1] + self.right[1]
        #self.print_state()

    def get_children(self):
        children = []
        actions = [[1, 0, 1], [2, 0, 1], [0, 1, 1], [1, 1, 1], [0, 2, 1]]
        for act in actions:
            child = NodeState(self, self.left[0], self.left[1], self.left[2], self.right[0], self.right[1], self.right[2])
            if(child.left[2] > 0):
                child.move_left(-1, act)
            else:
                child.move_left(1, act)
            if(child.is_valid()):
                children.append(child)
        return children

    def move_left(self, left, act):
        for i in range(len(act)):
            self.left[i] += left * act[i]
            self.right[i] -= left * act[i]

    def is_valid(self):
        if(self.left[0] not in range(0, self.max_m + 1) or self.right[0] not in range(0, self.max_m + 1)):
            return False
        if(self.left[1] not in range(0, self.max_c + 1) or self.right[1] not in range(0, self.max_c + 1)):
            return False
        if(self.left[2] not in range(0, 2) or self.right[2] not in range(0, 2)):
            return False
        if((self.left[0] < self.left[1] and self.left[0] > 0) or (self.right[0] < self.right[1] and self.right[0] > 0)):
            return False
        else:
            return True

    def print_state(self, file = None):
        if file != None:
            try:
                f = open(file, 'a')
                f.write("{},{},{}\n".format(self.left[0], self.left[1], self.left[2]))
                f.write("{},{},{}\n\n".format(self.right[0], self.right[1], self.right[2]))
            except:
                raise ValueError
        else:
            print("{},{},{}".format(self.left[0], self.left[1], self.left[2]))
            print("{},{},{}\n".format(self.right[0], self.right[1], self.right[2]))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            #return self.__dict__ == other.__dict__
            if self.left == other.left and self.right == other.right:
                return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


