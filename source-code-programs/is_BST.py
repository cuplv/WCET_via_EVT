# Python program to check if a binary tree is bst or not

INT_MAX = 4294967296
INT_MIN = -4294967296

# global variable prev - to keep track
# of previous node during Inorder
# traversal
prev = None


# A binary tree node
class Node:

	# Constructor to create a new node
	def __init__(self, data):
		self.data = data
		self.left = None
		self.right = None

# Returns true if the given tree is a binary search tree
# (efficient version)
def isBST_1(node):
	return (isBSTUtil(node, INT_MIN, INT_MAX))

# Retusn true if the given tree is a BST and its values
# >= min and <= max
def isBSTUtil(node, mini, maxi):

	# An empty tree is BST
	if node is None:
		return True

	# False if this node violates min/max constraint
	if node.data < mini or node.data > maxi:
		return False

	# Otherwise check the subtrees recursively
	# tightening the min or max constraint
	return (isBSTUtil(node.left, mini, node.data -1) and
		isBSTUtil(node.right, node.data+1, maxi))



# Returns true if given tree is BST.
def isBST_2(root, l = None, r = None):

	# Base condition
	if (root == None) :
		return True

	# if left node exist then check it has
	# correct data or not i.e. left node's data
	# should be less than root's data
	if (l != None and root.data <= l.data) :
		return False

	# if right node exist then check it has
	# correct data or not i.e. right node's data
	# should be greater than root's data
	if (r != None and root.data >= r.data) :
		return False

	# check recursively for every node.
	return isBST_2(root.left, l, root) and \
		isBST_2(root.right, root, r)



# function to check if given binary
# tree is BST
def isBST_3(root):

	# prev is a global variable
	global prev
	prev = None
	return isbst_rec(root)


# Helper function to test if binary
# tree is BST
# Traverse the tree in inorder fashion
# and keep track of previous node
# return true if tree is Binary
# search tree otherwise false
def isbst_rec(root):

	# prev is a global variable
	global prev

	# if tree is empty return true
	if root is None:
		return True

	if isbst_rec(root.left) is False:
		return False

	# if previous node'data is found
	# greater than the current node's
	# data return fals
	if prev is not None and prev.data > root.data:
		return False

	# store the current node in prev
	prev = root
	return isbst_rec(root.right)

def isBST_Tree(inp):
    # print(inp)
    arr = []
    for str in inp.split(" "):
        try:
            arr.append(int(str))
        except ValueError:
            pass
    if(len(arr) < 2):
        return False
    r = Node(arr[1])
    i = 2
    cur_root = r
    queue_roots = []
    while i < len(arr):
        if i %2 == 0:
            cur_root.left = Node(arr[i])
            queue_roots.append(cur_root.left)
        else:
            cur_root.right = Node(arr[i])
            queue_roots.append(cur_root.right)
            if len(queue_roots) > 0:
                cur_root = queue_roots.pop(0)
            else:
                return False
        i += 1
    # print(arr)
    if arr[0] % 3 == 0:
        isBST_1(r)
    elif arr[0] % 3 == 1:
        isBST_2(r)
    else:
        isBST_3(r)
    return True

# isBST_Tree("2 3")
# MAX_SIZE = 30       # for parameterize value, use the max value from xml file
# MAX_POP_SIZE = 1000
# MAX_POP_SIZE_TOT = 100000
# Actual_Time = False
# INPUT_SIZE = True   # paramterized inputs or not, True for array of values and False for a parameter value with XML file
# MIN_NUM_PATH = 5    # it is not used in clustering
# NUM_ITER = 1000
# TRIASL_EACH_ITER = 6000
# NUM_PARAMETERS = 15
# SIZE_INDEX = [0,1,5]
# CONSTANT_FACTOR = 2.0
# PERCENTAGE_TO_KEEP = 80   # in 100 scale
# DO_CLUSTERING = True
# STEPS_TO_DO_CLUSTERING = 1000
# STEPS_TO_KILL = STEPS_TO_DO_CLUSTERING * 5
# DEGREE_TO_FIT = 1
# NUM_CLUSTERS = 3
# MIN_NUM_PATH_PER_CLUST = 1  # have not used yet!
