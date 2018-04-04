import sys

# SOURCE: collaborated with John Gauthier
#         implementation ideas largely from Danny Yoo of UC Berkley on hashcollision.org

class RedBlackTree:

    class Node():
        def __init__(self, key=None,color='red'):
            self.right = None
            self.left = None
            self.p = None
            self.key = key
            self.color = color

    def __init__(self):
        self.NIL = self.Node(key = None, color='black')
        self.root = self.NIL
        self.size = 0
        self.ordered = []
        pass

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.p = x
        y.p = x.p
        if x.p == self.NIL:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.p = x
        y.p = x.p
        if x.p == self.NIL:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def insert(self, z):
        new_node = self.Node(key = z)
        self._insert(new_node)
        self.size += 1

    def _insert(self, z):
        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            if z.key < x.key :
                x = x.left
            else:
                x = x.right
        z.p = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.NIL
        z.right = self.NIL
        z.color = "red"
        self.rb_insert_fixup(z)

    def rb_insert_fixup(self, z):
        i = 0
        while z.p.color == "red":
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color == 'red':
                    z.p.color = "black"
                    y.color = "black"
                    z.p.p.color = "red"
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = 'black'
                    z.p.p.color = 'red'
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color == 'red':
                    z.p.color = "black"
                    y.color = "black"
                    z.p.p.color = "red"
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = 'black'
                    z.p.p.color = 'red'
                    self.left_rotate(z.p.p)
            i += 1
        self.root.color = 'black'

    def transplant(self, u, v):
        if u.p == self.NIL:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def remove(self, z):
        if self.size == 0:
            print("TreeError")
            return
        our_node = self.key_search(z)
        self._remove(our_node)
        self.size -= 1

    def _remove(self, z):
        y = z
        original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.right)
        else:
            y = self._min_node(z.right)
            original_color = y.color
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z,y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if original_color == 'black':
            self.rb_delete_fixup(x)

    def rb_delete_fixup(self, x):
        while x != self.root and x.color == 'black':
            if x == x.p.left:
                w = x.p.right
                if w.color == 'red':
                    w.color = 'black'
                    x.p.color = 'red'
                    self.left_rotate(x.p)
                    w = x.p.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.p
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == 'red':
                    w.color = 'black'
                    x.p.color = 'red'
                    self.right_rotate(x.p)
                    w = x.p.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.p
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(x.p)
                    x = self.root
        x.color = 'black'

    def search(self, x):
        return self._search(self.root, x)

    def _search(self, current_node, target):
        if current_node == self.NIL:
            return "NotFound"
        elif target == current_node.key:
            return "Found"
        elif target < current_node.key:
            return self._search(current_node.left, target)
        else:
            return self._search(current_node.right, target)

    def key_search(self, target):
        return self._key_search(self.root, target)

    def _key_search(self, current_node, target):
        if current_node == self.NIL:
            return None
        elif target == current_node.key:
            return current_node
        elif target < current_node.key:
            return self._key_search(current_node.left, target)
        else:
            return self._key_search(current_node.right, target)

    def maximum(self):
        if self.size == 0:
            return "Empty"
        return self._maximum(self.root)

    def _maximum(self, x):
        while x.right != self.NIL:
            x = x.right
        return x.key

    def minimum(self):
        if self.size == 0:
            return "Empty"
        return self._minimum(self.root)

    def _minimum(self, x):
        while x.left != self.NIL:
            x = x.left
        return x.key

    def _min_node(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def inprint(self):
        if self.size == 0:
            print("Empty")
            return
        self._inprint(self.root)
        for i in range(len(self.ordered)-1):
            print(self.ordered[i], end=' ')
        print(self.ordered[-1])
        self.ordered = []

    def _inprint(self, x):
        if x != self.NIL and x.key != None:
            self._inprint(x.left)
            self.ordered.append(x.key)
            self._inprint(x.right)

'''
rb = RedBlackTree()
rb.insert(1)
rb.inprint()
print()
rb.insert(2)
rb.inprint()
print()
rb.insert(3)
rb.inprint()
print()
rb.insert(10)
rb.insert(5)
rb.inprint()
print()
print()
rb.remove(5)
rb.inprint()
'''

def driver():
    rb = RedBlackTree()
    with open(sys.argv[1]) as f:
        n = int(f.readline().strip())
        for _ in range(n):
            data_line = f.readline().strip().split()
            action = data_line[0]
            #print(action)
            #(data_line)
            if action == "insert":
                #print(data_line[1])
                rb.insert(int(data_line[1]))
            elif action == "remove":
                rb.remove(int(data_line[1]))
            elif action == "search":
                print(rb.search(int(data_line[1])))
            elif action == "max":
                print(rb.maximum())
            elif action == "min":
                print(rb.minimum())
            elif action == "inprint":
                rb.inprint()
    pass

if __name__ == '__main__':
    driver()
