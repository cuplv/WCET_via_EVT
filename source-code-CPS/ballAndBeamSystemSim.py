from NeuralODE import NeuralODE
from NeuralNetwork import NeuralNetwork, read_network_from_sherlock_file
import numpy as np
import sys 
from typing import List, Tuple 

def ball_and_beam_ode(x: List[float], u: List[float], w: List[float]):
    dx0 = x[1]
    dx1 = -9.8 * np.sin(x[2]) + x[0]*(x[3]**2) + 0.05*w[0]
    dx2 = x[3]
    dx3 = u[0] - 10
    return [dx0, dx1, dx2, dx3]

def doit(n_sims: int, output_file_name: str):
    state_ranges = [(-1, 1), (-1,1), (-0.2, 0.2), (-0.1, 0.1)]
    nn = read_network_from_sherlock_file('networks/controller_network_ball_and_beam.nt')
    node = NeuralODE(nn,ball_and_beam_ode,4,1,[(-1,1)])
    traces = node.simulate_for_random_initial_conditions(state_ranges,30.0, 0.02, n_sims)
    stable_ranges= [(-0.05, 0.05), (-0.05, 0.05),(-0.05,0.05),(-0.05,0.05)]
    stab_times= [node.get_stabilization_time(time_points, tr, stable_ranges) for (time_points, tr) in traces]
    f = open(output_file_name, 'a')
    for t in stab_times: 
        print(t, file=f)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2: 
        print(f'{sys.argv[0]} <num sims> <output filename> ')
        sys.exit(1)
    n_sims = int(sys.argv[1])
    output_file = sys.argv[2]
    print(f'running {n_sims} simulations -- output timings to {output_file}')
    doit(n_sims, output_file)

