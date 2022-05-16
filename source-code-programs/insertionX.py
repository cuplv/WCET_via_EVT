# the optimized insertion sort!# the optimized insertion sort!# the optimized insertion sort!

def insertionXSort(a,n):
        # put smallest element in position to serve as sentinel
        exchanges = 0;
        i = n - 1
        while i > 0:
            if a[i] < a[i-1]:
                tmp = a[i]
                a[i] = a[i-1]
                a[i-1] = tmp
                exchanges += 1
            i -= 1
        if exchanges == 0:
            return

        # insertion sort with half-exchanges
        i = 2
        while i < n:
            v = a[i];
            j = i;
            while v < a[j-1]:
                a[j] = a[j-1]
                j -= 1
            a[j] = v
            i += 1
        return a


def insertionX(inp):
    #print("you are calling insertionX")
    arr = []
    for str in inp.split(" "):
        try:
            arr.append(int(str))
        except ValueError:
            pass
    n = len(arr)
    if(n < 2):
        return False
    a_res = insertionXSort(arr,n)
    #print(a_res)
    return True

#insertionX("1 -1 3 5 0")

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
# NUM_CLUSTERS = 3
# MIN_NUM_PATH_PER_CLUST = 1  # have not used yet!
