# Python code to implement iterative Binary
# Search.

def mergeSortHelper(arr):
    if len(arr) >1:
        mid = len(arr)//2 #Finding the mid of the array
        L = arr[:mid] # Dividing the array elements
        R = arr[mid:] # into 2 halves

        mergeSortHelper(L) # Sorting the first half
        mergeSortHelper(R) # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i+=1
            else:
                arr[k] = R[j]
                j+=1
            k+=1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i+=1
            k+=1

        while j < len(R):
            arr[k] = R[j]
            j+=1
            k+=1


# It returns location of x in given array arr
# if present, else returns -1
def binarySearchHelper(arr, l, r, x):

	while l <= r:

		mid = l + (r - l)/2;

		# Check if x is present at mid
		if arr[mid] == x:
			return mid

		# If x is greater, ignore left half
		elif arr[mid] < x:
			l = mid + 1

		# If x is smaller, ignore right half
		else:
			r = mid - 1
	# If we reach here, then the element
	# was not present
	return 1


def binarySearch(inp):
	arr = []
	for str in inp.split(" "):
		try:
			arr.append(int(str))
		except ValueError:
			pass
	if(len(arr) < 1):
		return False
	val_to_find = 5
	is_exist = [1 for x in arr if x == val_to_find]
	mergeSortHelper(arr)
	# print(arr)
	if len(is_exist) > 0:
		binarySearchHelper(arr, 0, len(arr)-1, val_to_find)

# binarySearch("1 -2 3 4 0")
