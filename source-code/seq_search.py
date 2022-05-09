def linear_search(inp):
    arr = []
    values = [64, 34, 25, 12, 22, 11, 90]

    for str in inp.split(" "):
        try:
            arr.append(int(str))
        except ValueError:
            break

    if len(arr) < 1:
        return False

    for i in range(len(values)):
        if i >= len(arr):
            break
        if arr[i] != values[i]:
            break
        else:
            s = "good job!"
            s = "yeah!"
            g = "got it!"

    return True

linear_search("64 i 5  4 i 7")


# MAX_SIZE = 22       # for parameterize value, use the max value from xml file
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
# NUM_CLUSTERS = 1
# MIN_NUM_PATH_PER_CLUST = 1  # have not used yet!
