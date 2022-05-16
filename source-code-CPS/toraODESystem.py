from NeuralODE import NeuralODE
from NeuralNetwork import NeuralNetwork, read_network_from_sherlock_file
import numpy as np
import sys 
from typing import List, Tuple 

def tora_ode(x: List[float], u: List[float], w: List[float]):
    dx0 = x[1]
    dx1 = -x[0] + 0.1 * np.sin(x[2]) + w[0]
    dx2 = x[3]
    dx3 = u[0] - 10.0
    return [dx0, dx1, dx2, dx3]

def doit(n_sims: int, output_file_name: str, tiny: bool = True):
    state_ranges = [(-1, 1), (-1,1), (-0.5, 0.5), (-0.5, 0.5)]
    nn = read_network_from_sherlock_file('networks/tora_tiny_controller.nt') if tiny else read_network_from_sherlock_file('networks/tora_giant_controller.nt')
    node = NeuralODE(nn, tora_ode, 4, 1, [(-0.01,0.01)])
    traces = node.simulate_for_random_initial_conditions(state_ranges,300.0, 0.02, n_sims)
    stable_ranges= [(-0.1, 0.1), (-0.1, 0.1),(-0.1,0.1),(-0.1,0.1)]
    stab_times= [node.get_stabilization_time(time_points, tr, stable_ranges) for (time_points, tr) in traces]
    f = open(output_file_name, 'a')
    for t in stab_times: 
        print(t, file=f)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 3: 
        print(f'{sys.argv[0]} <num sims> <output filename> <g or t for giant or tiny>')
        sys.exit(1)
    n_sims = int(sys.argv[1])
    output_file = sys.argv[2]
    tiny = sys.argv[3] == 't'
    print(f'running {n_sims} simulations with tiny = {tiny} -- output timings to {output_file}')
    doit(n_sims, output_file, tiny)

