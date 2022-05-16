import sys
from typing import List, Dict
from io import TextIOWrapper


class NetworkNode:
    # Represent a neural network node
    # The attributes to a node include
    # ID: A numerical ID for the node
    # node_type: What type of node is it and what is its activation function
    # incoming_connections: a list of weights and ids for nodes that are incoming
    # outgoing_connections: a list of weights and ids for nodes that are outgoing
    def __init__(self, id: int, node_type: str):
        self._id = id
        self._node_type = node_type
        self._incoming = []
        self._bias = 0.0

    def get_id(self) -> int:
        return self._id

    def get_incoming(self):
        return self._incoming

    def get_bias(self):
        return self._bias

    def add_incoming_connection(self, w: float, prev_node):
        self._incoming.append((w, prev_node))  # append a pair containing a weight an node reference

    def add_outgoing_connection(self, w: float, next_node):
        self._outgoing.append((w, next_node))  # append a pair containing weight and node reference

    def add_bias(self, b: float):
        self._bias = b

    def evaluate_node(self, eval_map: Dict[int, float]) -> float:
        v = self._bias
        for (w, prev_node) in self._incoming:
            prev_node_id = prev_node.get_id()
            assert (prev_node_id in eval_map)
            v = v + w * eval_map[prev_node_id]
        v = max(0.0, v) # apply the RELU
        return v

    def dump_node_dot(self, fHandle: TextIOWrapper):
        print('n%d' % self._id, file=fHandle, end='')
        if self._node_type == 'INPUT':
            print('[shape=diamond, fillcolor=red, label=\"INP%d\"];' % self._id, file=fHandle)
        elif self._node_type == 'OUTPUT':
            print('[shape=circle, fillcolor=blue, label=\"%f\"];' % self._bias, file=fHandle)
        else:
            print('[shape=box, label=\"%f\"];' % self._bias, file=fHandle)
        return

    def dump_edges_dot(self, fHandle: TextIOWrapper):
        for (w, prev) in self._incoming:
            print('n%d -> n%d [label=%f];' % (prev.get_id(), self.get_id(), w), file=fHandle)
        return
