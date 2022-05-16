import myUtils
from typing import List, Tuple 
import sys
from NeuralNetwork import NeuralNetwork
from scipy.integrate import odeint 
import numpy as np 
from numpy import random 
from datetime import datetime

class NeuralODE:
    def __init__(self, network_handle:NeuralNetwork, 
                ode_fun, 
                num_states: int, num_ctrl:int, 
                disturbance_ranges: List[Tuple[float, float]]):
        assert network_handle.get_num_inputs() == num_states 
        assert network_handle.get_num_outputs() == num_ctrl 
        self.nn = network_handle
        self.ode_fun = ode_fun 
        self.n = num_states 
        self.m = num_ctrl 
        self.w = len(disturbance_ranges)
        self.w_ranges = disturbance_ranges
        self.rng = random.default_rng(int(datetime.now().timestamp()))

    
    def get_random_disturbances(self):
        return [random.uniform(l, u) for (l,u) in self.w_ranges]
    
    def simulate(self, time_horiz:float, x0: List[float], tstep:float = 0.01):
        assert len(x0) == self.n
        def ode_function(t:float, x: List[float]) -> List[float]:
            u = self.nn.eval_network(x)
            w = self.get_random_disturbances()
            dx= self.ode_fun(x, u, w)
            return dx 
        time_points = np.arange(0.0, time_horiz, tstep)
        cur_state = x0
        result = [x0]
        for t in time_points: 
            deriv = ode_function(t, cur_state)
            new_state = [x + tstep * dx for (x,dx) in zip(cur_state, deriv)]
            result.append(new_state)
            cur_state = new_state 
        return (time_points, result)

    def simulate_for_random_initial_conditions(self, x0_ranges: List[float], 
                                                t_horiz:float, tstep:float =0.01, n_sims:int=1000):
        assert len(x0_ranges) == self.n
        def get_random_x0():
            return [random.uniform(l,u) for (l,u) in x0_ranges]
        return [self.simulate(t_horiz, get_random_x0(), tstep) for _ in range(n_sims)]

    def get_stabilization_time(self, time_points, trace, stable_ranges):
        # find the latest time point beyond which the trace stays entirely inside the range.
        def in_range(x):
            assert len(x) == len(stable_ranges)
            return all( l <= xi and xi <= u for (xi, (l,u)) in zip(x, stable_ranges) )
        try: 
            last_idx = next(i for i in reversed(range(len(trace))) if not in_range(trace[i]))
        except StopIteration: 
            last_idx = 0
        return time_points[last_idx] if last_idx < len(time_points) else time_points[-1]

    def get_stabilization_times(self, stable_ranges,
                                x0_ranges: List[float], 
                                t_horiz:float, 
                                tstep:float =0.01, 
                                n_sims:int=1000 ):
        
        all_sims = self.simulate_for_random_initial_conditions(x0_ranges, t_horiz, tstep, n_sims)
        return [ 
            self.get_stabilization_time(time_points, trace, stable_ranges) 
            for (time_points,trace) in all_sims
        ]