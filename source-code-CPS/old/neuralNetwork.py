from NetworkNode import NetworkNode
import myUtils
from typing import List
import sys
from io import TextIOWrapper

class NeuralNetwork:

    def __init__(self, n_inputs, n_outputs, n_hidden, hidden_layer_sizes):
        self._n_nodes = 0
        self._n_inputs = n_inputs
        self._n_outputs = n_outputs
        self._n_hidden = n_hidden
        self._hidden_layer_sizes = hidden_layer_sizes
        self._input_nodes = []
        self._output_nodes = []
        self._hidden_layer_neuron_id_map = {}  # Dictionary mapping (hidden layer number ,
        self._all_nodes = {}  # Dictionary mapping id to node references

    def get_num_inputs(self) -> int:
        return self._n_inputs

    def get_output_node(self, idx: int) -> NetworkNode:
        assert(0 <= idx < self._n_outputs)
        return self._output_nodes[idx]

    def get_input_node(self, idx: int) -> NetworkNode:
        assert(0 <= idx < self._n_inputs)
        return self._input_nodes[idx]

    def get_input_nodes(self) -> List[NetworkNode]:
        return self._input_nodes

    def get_output_nodes(self) -> List[NetworkNode]:
        return self._output_nodes

    def get_hidden_layer_node(self, layer_id: int, node_idx: int) -> NetworkNode:
        assert(0 <= layer_id <= self._n_hidden)
        if 0 <= layer_id < self._n_hidden:
            num_nodes_in_layer = self._hidden_layer_sizes[layer_id]
        else:
            num_nodes_in_layer = self._n_outputs
        assert (0 <= node_idx < num_nodes_in_layer)
        assert (layer_id, node_idx) in self._hidden_layer_neuron_id_map
        return self._hidden_layer_neuron_id_map[(layer_id, node_idx)]

    def add_node(self, node_type: str) -> (int, NetworkNode):
        assert(myUtils.isValidNodetype(node_type))
        node_id = self._n_nodes
        self._n_nodes = self._n_nodes + 1
        node_ref = NetworkNode(node_id, node_type)
        if node_type == 'INPUT':
            self._input_nodes.append(node_ref)
        if node_type == 'OUTPUT':
            self._output_nodes.append(node_ref)
        self._all_nodes[node_id] = node_ref
        return node_id, node_ref

    def register_hidden_layer_node(self, layer_id: int, layer_node_num: int, node_ref: NetworkNode):
        assert(0 <= layer_id <= self._n_hidden) # if layer_id == self._n_hidden we will treat it as a output node
        if layer_id < self._n_hidden:
            node_idx_max = self._hidden_layer_sizes[layer_id]
        else:
            node_idx_max = self._n_outputs
        assert(0 <= layer_node_num < node_idx_max)
        self._hidden_layer_neuron_id_map[(layer_id, layer_node_num)] = node_ref

    def num_hidden_layers(self) -> int:
        return self._n_hidden

    def get_num_nodes_in_hidden_layer(self, layer_id) -> int:
        assert (0 <= layer_id < self._n_hidden)
        return self._hidden_layer_sizes[layer_id]

    def add_weights_and_biases(self, node: NetworkNode, list_of_weights: List[float], bias: float, cur_layer: int):
        node.add_bias(bias)
        if cur_layer == 0:
            prev_layer = self._input_nodes
        else:
            assert (0 < cur_layer <= self._n_hidden)
            prev_layer = [
                self._hidden_layer_neuron_id_map[(cur_layer-1, j)]
                for j in range(self.get_num_nodes_in_hidden_layer(cur_layer-1))
            ]

        num_weights = len(list_of_weights)
        assert(len(prev_layer) == num_weights)
        for j in range(num_weights):
            node.add_incoming_connection(list_of_weights[j], prev_layer[j])

    def dump_dot(self, fHandle: TextIOWrapper):
        print('digraph NN{ ', file=fHandle)
        for node_ref in self._all_nodes.values():
            node_ref.dump_node_dot(fHandle)
        for node_ref in self._all_nodes.values():
            node_ref.dump_edges_dot(fHandle)
        print('}', file=fHandle)

    def eval_network(self, input_values: List[float]) -> List[float]:
        assert(len(input_values) == self._n_inputs)
        eval_map = {}
        for j in range(self._n_inputs):
            inp_node_ref = self._input_nodes[j]
            inp_node_id = inp_node_ref.get_id()
            eval_map[inp_node_id] = input_values[j]
        for layer_id in range(self._n_hidden+1):
            if layer_id < self._n_hidden:
                node_idx_max = self._hidden_layer_sizes[layer_id]
            else:
                node_idx_max = self._n_outputs
            for node_idx in range(node_idx_max):
                node_ref = self.get_hidden_layer_node(layer_id, node_idx)
                k = node_ref.get_id()
                assert (k in self._all_nodes)
                assert (k not in eval_map)
                out_val = node_ref.evaluate_node(eval_map)
                eval_map[k] = out_val
        output_values = []
        for oNode in self._output_nodes:
            oNode_id = oNode.get_id()
            assert (oNode_id in eval_map)
            output_values.append(eval_map[oNode_id])
        return output_values


# This function will read a sherlock formatted network file
def read_network_from_sherlock_file(fileName: str) -> NeuralNetwork:
    try:
        f = open(fileName, 'r')
        n_inputs = int(f.readline())  # Read number of inputs
        n_outputs = int(f.readline())  # Read number of outputs
        n_hidden_layers = int(f.readline())  # Read number of hidden layers
        hidden_layer_sizes = []  # Read the size of each hidden layer
        for j in range(n_hidden_layers):
            layer_size = int(f.readline())
            hidden_layer_sizes.append(layer_size)
        # Create the data structure
        neural_net = NeuralNetwork(n_inputs, n_outputs, n_hidden_layers, hidden_layer_sizes)
        # Create input nodes
        for j in range(n_inputs):
            neural_net.add_node('INPUT')
        # Create output nodes
        for j in range(n_outputs):
            neural_net.add_node('OUTPUT')
        # Read the weights and make the connections
        for layer_id in range(n_hidden_layers):
            if layer_id == 0:  # is this the very first layer?
                prev_layer_size = n_inputs  # if yes then the inputs are the previous layer.
            else:
                prev_layer_size = hidden_layer_sizes[layer_id - 1]
            for node_index in range(hidden_layer_sizes[layer_id]):
                (node_id, node_ref) = neural_net.add_node('RELU')
                neural_net.register_hidden_layer_node(layer_id, node_index, node_ref)
                weights_list = []
                for k in range(prev_layer_size):  # Read all the weights
                    weights_list.append(float(f.readline()))
                bias = float(f.readline())  # Read the bias
                neural_net.add_weights_and_biases(node_ref, weights_list, bias, layer_id)
        # Finally for the output layers
        layer_id = n_hidden_layers # This will signal our code that we are reading the output layers
        prev_layer_size = hidden_layer_sizes[layer_id - 1]
        for node_index in range(n_outputs):
            node_ref = neural_net.get_output_node(node_index)
            neural_net.register_hidden_layer_node(layer_id, node_index, node_ref)
            weights_list = []
            for k in range(prev_layer_size):
                weights_list.append(float(f.readline()))
            bias = float(f.readline())
            neural_net.add_weights_and_biases(node_ref, weights_list, bias, layer_id)
        f.close()
        # Done? Let us return the network we created
        return neural_net
    except IOError:
        print('Error reading file %s' % fileName)
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage: python3 %s <name of sherlock network file>' % sys.argv[0])
    else:
        nnet = read_network_from_sherlock_file(sys.argv[1])
        if len(sys.argv) >= 3:
            outFileName = sys.argv[2]
        else:
            outFileName = 'output.dot'
        fHandle = open(outFileName, 'w')
        nnet.dump_dot(fHandle)
        fHandle.close()


