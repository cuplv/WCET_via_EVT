# Python program for implementation of MergeSort

# Code to print the list
def printList(arr):
    for i in range(len(arr)):
        print(arr[i])

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
    # print(arr)
    return True


def mergeSort(inp):
    arr = []
    for str in inp.split(" "):
        try:
            arr.append(int(str))
        except ValueError:
            return False
    if len(arr) < 1:
        return False

    mergeSortHelper(arr)

# mergeSort(" ")
