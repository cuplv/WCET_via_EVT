import random
import time
# Python program for implementation of Quicksort


# This function is same in both iterative and recursive
def partition(a,l,r):
   x, j, t = a[l], l, r
   i = j

   while i <= t :
      if a[i] < x:
         a[j], a[i] = a[i], a[j]
         j += 1

      elif a[i] > x:
         a[t], a[i] = a[i], a[t]
         t -= 1
         i -= 1 # remain in the same i in this case
      i += 1
   return j, t

# Function to do Quick sort
# arr[] --> Array to be sorted,
# l  --> Starting index,
# h  --> Ending index
def quickSortIterative(arr,l,h):

    # Create an auxiliary stack
    size = h - l + 1
    stack = [0] * (size)

    # initialize top of stack
    top = -1

    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    # Keep popping from stack while is not empty
    while top >= 0:

        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        i,j = partition( arr, l, h )

        # If there are elements on left side of pivot,
        # then push left side to stack
        if i-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = i-1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if j+1 < h:
            top = top + 1
            stack[top] = j+1
            top = top + 1
            stack[top] = h

def quickSortThreeways(inp):
    arr = []
    for str in inp.split(" "):
        try:
            arr.append(int(str))
        except ValueError:
            pass
    l = 0
    h = len(arr)
    if(h < 2):
        return False
    quickSortIterative(arr, l, h-1)
    return True

# quickSort("1 1 -1 2 2")
