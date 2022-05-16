
# TODO: Need to fix Souradeep semantics which gratuitously puts a RELU at the output of the NN.
def isValidNodetype(ntype: str):
    return ntype == 'INPUT' or ntype == 'OUTPUT' or ntype == 'RELU'

