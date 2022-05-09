# Python program to demonstrate insert operation in binary search tree

# A utility class that represents an individual node in a BST
class Node:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key

# A utility function to insert a new node with the given key
def insert(root,node):
    if root is None:
        root = node
    else:
        if root.val < node.val:
            if root.right is None:
                root.right = node
            else:
                insert(root.right, node)
        else:
            if root.left is None:
                root.left = node
            else:
                insert(root.left, node)

# A utility function to do inorder tree traversal
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)

def BST_insert(inp):
    arr = []
    for str in inp.split(" "):
        try:
            arr.append(int(str))
        except ValueError:
            pass
    if(len(arr) < 1):
        return False
    r = Node(arr[0])
    i = 1
    while i < len(arr):
        insert(r,Node(arr[i]))
        i += 1
    return True

# BST_insert("3 1 2 4 5 6")

# MAX_SIZE = 30       # for parameterize value, use the max value from xml file
# MAX_POP_SIZE = 1000
# MAX_POP_SIZE_TOT = 100000
# Actual_Time = False
# INPUT_SIZE = True   # paramterized inputs or not, True for array of values and False for a parameter value with XML file
# MIN_NUM_PATH = 5    # it is not used in clustering
# NUM_ITER = 1000
# TRIASL_EACH_ITER = 2000
# NUM_PARAMETERS = 15
# SIZE_INDEX = [0,1,5]
# CONSTANT_FACTOR = 2.0
# PERCENTAGE_TO_KEEP = 80   # in 100 scale
# DO_CLUSTERING = True
# STEPS_TO_DO_CLUSTERING = 1000
# STEPS_TO_KILL = STEPS_TO_DO_CLUSTERING * 5
# DEGREE_TO_FIT = 1
# NUM_CLUSTERS = 2
# MIN_NUM_PATH_PER_CLUST = 1  # have not used yet!
