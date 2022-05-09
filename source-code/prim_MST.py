# A Python program for Prims's MST for
# adjacency list representation of graph

from collections import defaultdict
import sys

class Heap():

	def __init__(self):
		self.array = []
		self.size = 0
		self.pos = []

	def newMinHeapNode(self, v, dist):
		minHeapNode = [v, dist]
		return minHeapNode

	# A utility function to swap two nodes of
	# min heap. Needed for min heapify
	def swapMinHeapNode(self, a, b):
		t = self.array[a]
		self.array[a] = self.array[b]
		self.array[b] = t

	# A standard function to heapify at given idx
	# This function also updates position of nodes
	# when they are swapped. Position is needed
	# for decreaseKey()
	def minHeapify(self, idx):
		smallest = idx
		left = 2 * idx + 1
		right = 2 * idx + 2

		if left < self.size and self.array[left][1] < \
								self.array[smallest][1]:
			smallest = left

		if right < self.size and self.array[right][1] < \
								self.array[smallest][1]:
			smallest = right

		# The nodes to be swapped in min heap
		# if idx is not smallest
		if smallest != idx:

			# Swap positions
			self.pos[ self.array[smallest][0] ] = idx
			self.pos[ self.array[idx][0] ] = smallest

			# Swap nodes
			self.swapMinHeapNode(smallest, idx)

			self.minHeapify(smallest)

	# Standard function to extract minimum node from heap
	def extractMin(self):

		# Return NULL wif heap is empty
		if self.isEmpty() == True:
			return

		# Store the root node
		root = self.array[0]

		# Replace root node with last node
		lastNode = self.array[self.size - 1]
		self.array[0] = lastNode

		# Update position of last node
		self.pos[lastNode[0]] = 0
		self.pos[root[0]] = self.size - 1

		# Reduce heap size and heapify root
		self.size -= 1
		self.minHeapify(0)

		return root

	def isEmpty(self):
		return True if self.size == 0 else False

	def decreaseKey(self, v, dist):

		# Get the index of v in heap array

		i = self.pos[v]

		# Get the node and update its dist value
		self.array[i][1] = dist

		# Travel up while the complete tree is not
		# hepified. This is a O(Logn) loop
		while i > 0 and self.array[i][1] < \
					self.array[(i - 1) / 2][1]:

			# Swap this node with its parent
			self.pos[ self.array[i][0] ] = (i-1)/2
			self.pos[ self.array[(i-1)/2][0] ] = i
			self.swapMinHeapNode(i, (i - 1)/2 )

			# move to parent index
			i = (i - 1) / 2;

	# A utility function to check if a given vertex
	# 'v' is in min heap or not
	def isInMinHeap(self, v):

		if self.pos[v] < self.size:
			return True
		return False


def printArr(parent, n):
	for i in range(1, n):
		print "% d - % d" % (parent[i], i)


class Graph():

	def __init__(self, V):
		self.V = V
		self.graph = defaultdict(list)

	def BFS(self, s):
		# Mark all the vertices as not visited
		visited = [False] * (len(self.graph))

		# Create a queue for BFS
		queue = []

		# Mark the source node as
		# visited and enqueue it
		queue.append(s)
		visited[s] = True

		while queue:
			# print(queue)
			# Dequeue a vertex from
			# queue and print it
			s = queue.pop(0)

			# Get all adjacent vertices of the
			# dequeued vertex s. If a adjacent
			# has not been visited, then mark it
			# visited and enqueue it
			for i,j in self.graph[s]:
				if visited[i] == False:
					queue.append(i)
					visited[i] = True
		return visited

	# Adds an edge to an undirected graph
	def addEdge(self, src, dest, weight):

		# Add an edge from src to dest. A new node is
		# added to the adjacency list of src. The node
		# is added at the begining. The first element of
		# the node has the destination and the second
		# elements has the weight
		newNode = [dest, weight]
		self.graph[src].insert(0, newNode)

		# Since graph is undirected, add an edge from
		# dest to src also
		newNode = [src, weight]
		self.graph[dest].insert(0, newNode)

	# The main function that prints the Minimum
	# Spanning Tree(MST) using the Prim's Algorithm.
	# It is a O(ELogV) function
	def PrimMST(self):
		# Get the number of vertices in graph
		V = self.V

		# key values used to pick minimum weight edge in cut
		key = []

		# List to store contructed MST
		parent = []

		# minHeap represents set E
		minHeap = Heap()

		# Initialize min heap with all vertices. Key values of all
		# vertices (except the 0th vertex) is is initially infinite
		for v in range(V):
			parent.append(-1)
			key.append(sys.maxint)
			minHeap.array.append( minHeap.newMinHeapNode(v, key[v]) )
			minHeap.pos.append(v)

		# Make key value of 0th vertex as 0 so
		# that it is extracted first
		minHeap.pos[0] = 0
		key[0] = 0
		minHeap.decreaseKey(0, key[0])

		# Initially size of min heap is equal to V
		minHeap.size = V;

		# In the following loop, min heap contains all nodes
		# not yet added in the MST.
		while minHeap.isEmpty() == False:

			# Extract the vertex with minimum distance value
			newHeapNode = minHeap.extractMin()
			u = newHeapNode[0]

			# Traverse through all adjacent vertices of u
			# (the extracted vertex) and update their
			# distance values
			for pCrawl in self.graph[u]:

				v = pCrawl[0]

				# If shortest distance to v is not finalized
				# yet, and distance to v through u is less than
				# its previously calculated distance
				if minHeap.isInMinHeap(v) and pCrawl[1] < key[v]:
					key[v] = pCrawl[1]
					parent[v] = u

					# update distance value in min heap also
					minHeap.decreaseKey(v, key[v])

		# printArr(parent, V)

def primMST(inp):
	arr = []
	node = []
	weight = []
	i = 1
	for str in inp.split(" "):
	    try:
	        arr.append(int(str))
	        if i % 3 == 0:
	            weight.append(int(str))
	        else:
	            node.append(int(str))
	        i += 1
	    except ValueError:
	        pass
	if len(node) < 4 or len(weight) < 2:
	    return False
	bad_weight = [val for val in weight if val <= 0]
	bad_index = [val for val in node if val < 0]
	if len(bad_weight) > 0 or len(bad_index) > 0:
	    return False
	while (len(node)+1)/2 > len(weight):
	    node.pop(len(node)-1)
	diff_nodes = set(node)
	not_good_vals = [val for val in diff_nodes if val >= len(diff_nodes)]
	gen = [x for x in not_good_vals if x != 0]
	if len(gen) >= 1:
	    # print("here2")
	    poss_index = [j for j in range(len(set(node))) if j not in diff_nodes]
	    for j in poss_index:
	        for val in gen:
	            node = [j if val == value else value for value in node]
	            gen.remove(val)
	            break
	# node = [j if val == value else value for value in node for val in gen for j in poss_index]
	# print(arr)
	# print(node)
	# print(weight)
	# print(gen)
	# if len(gen) >= 1:
	#     print(poss_index)
	#
	# for val in gen:
	#
	#     for j in poss_index:
	#         break
	#     diff_nodes = set(node)

	graph = Graph(len(set(node)))


	i = 0
	j = 0
	while i < len(node) - 1:
	    if node[i] == node[i+1]:
	        return False
	    graph.addEdge(node[i], node[i+1], weight[j])
	    i += 2
	    j += 1
	# print("here4")
	res = graph.BFS(node[0])
	res_connected = [-1 for x in res if x == False]
	if len(res_connected) == 0:
	    # print("not connected!")
		graph.PrimMST()
	# print("here5")
	return True


# primMST("0 1 4 0 7 8 1 2 8 1 7 11 2 3 7 2 8 2 2 5 4 3 4 9 3 5 14 4 5 10 5 6 2 6 7 1 6 8 6 7 8 7")
# primMST("0 1 4 2 3 8 4 5 8 6 7 1 8 9 7 10 11 2 12 13 4 14 15 9 16 17 14 18 19 10 20 21 2 22 23 1 24 25 6")

# primMST("0 1 4 2 3 3 4 5 5")

# MAX_SIZE = 38       # for parameterize value, use the max value from xml file
# MAX_POP_SIZE = 1000
# MAX_POP_SIZE_TOT = 100000
# Actual_Time = False
# INPUT_SIZE = True   # paramterized inputs or not, True for array of values and False for a parameter value with XML file
# MIN_NUM_PATH = 5    # it is not used in clustering
# NUM_ITER = 1000
# TRIASL_EACH_ITER = 10000
# NUM_PARAMETERS = 15
# SIZE_INDEX = [0,1,5]
# CONSTANT_FACTOR = 2.0
# PERCENTAGE_TO_KEEP = 80   # in 100 scale
# DO_CLUSTERING = True
# STEPS_TO_DO_CLUSTERING = 1000
# STEPS_TO_KILL = STEPS_TO_DO_CLUSTERING * 5
# DEGREE_TO_FIT = 1
# NUM_CLUSTERS = 5
# MIN_NUM_PATH_PER_CLUST = 1  # have not used yet!
