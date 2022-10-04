import sys
import math
import random
import os
import time
import subprocess32 as subprocess
import numpy as np
from scipy.stats import norm
from Timeout import timeout

# To do: Sep 16: add time profile for each input! (extra column in the CSV file)

import quick_sort, insertionX, seq_search, qsort_threeways, BST_insert
import merge_sort, prim_MST, Boyer_Moore, is_BST, binary_search
# import bm_chaos, pairwise_distance, dbscan_driver
# import TreeRegressor
# import LogisticRegression
# import Discriminant_Analysis
# import TreeRegressor
# import spectral_clustering
# import minibatch_kmeans

MAX_SIZE = 10       # for parameterize value, use the max value from xml file
Actual_Time = True
INPUT_SIZE = True   # paramterized inputs or not, True for array of values and False for a parameter value with XML file
NUM_ITER = 2000
TRIASL_EACH_ITER = 255
ITER_to_Model = 25
# False for Booyer_moore
Only_Num = True

input_program = quick_sort.quickSort
#input_program = insertionX.insertionX
#input_program = qsort_threeways.quickSortThreeways
#input_program = seq_search.linear_search
#input_program = is_BST.isBST_Tree
#input_program = BST_insert.BST_insert
#input_program = merge_sort.mergeSort
#input_program = Boyer_Moore.BoyerMoore
#input_program = binary_search.binarySearch
#input_program = prim_MST.primMST
#input_program = rbtree.rbtreeHelper
#input_program = test1.test1
#input_program = bm_chaos.bm_chaos
#input_program = pairwise_distance.pairwise_distance
#input_program = dbscan_driver.dbscan_driver
#input_program_tree = 'dbscan_Params.xml'
# input_program = TreeRegressor.TreeRegress
# input_program_tree = 'TreeRegressor_Params.xml'
# input_program = LogisticRegression.logistic_regression
# input_program_tree = 'logistic_regression_Params.xml'
# input_program = Discriminant_Analysis.disc_analysis
# input_program_tree = 'Discriminant_Analysis_Params.xml'
# input_program = TreeRegressor.TreeRegress
# input_program_tree = 'TreeRegressor_Params.xml'
# input_program = spectral_clustering.spectral_clustering
# input_program_tree = 'spectral_clustering_Params.xml'
# input_program = minibatch_kmeans.minibatch_kmeans
# input_program_tree = 'minibatch_kmeans_Params.xml'

class Coverage(object):
    # Trace function
    def traceit(self, frame, event, arg):
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        if event == "line":
            function_name = frame.f_code.co_name
            lineno = frame.f_lineno
            self._trace.append((function_name, lineno))

        return self.traceit

    def __init__(self):
        self._trace = []

    # Start of `with` block
    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)


    def trace(self):
        """The list of executed lines, as (function_name, line_number) pairs"""
        return self._trace

    def coverage(self):
        """The set of executed lines, as (function_name, line_number) pairs"""
        path = set()
        for str, line in self.trace():
            path.add(line)
        path_sign = 0
        for line in path:
            path_sign ^= line
        return path_sign, len(self.trace())

from functools import wraps
import errno
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError("time_error")

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


class Runner(object):
    # Test outcomes
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"

    def __init__(self):
        """Initialize"""
        pass

    def run(self, inp):
        """Run the runner with the given input"""
        return (inp, Runner.UNRESOLVED)

class PrintRunner(Runner):
    def run(self, inp):
        """Print the given input"""
        print(inp)
        return (inp, Runner.UNRESOLVED)

class ProgramRunner(Runner):
    def __init__(self, program):
        """Initialize.  `program` is a program spec as passed to `subprocess.run()`"""
        self.program = program
        self.time_cost = 0
    def run_process(self, inp=""):
        """Run the program with `inp` as input.  Return result of `subprocess.run()`."""
        res = subprocess.run(self.program,
                              input=inp,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True)
        return res

    def run(self, inp=""):
        """Run the program with `inp` as input.  Return test outcome based on result of `subprocess.run()`."""
        result = self.run_process(inp)

        if result.returncode == 0:
            outcome = self.PASS
        elif result.returncode < 0:
            outcome = self.FAIL
        else:
            outcome = self.UNRESOLVED


class Fuzzer(object):
    def __init__(self):
        self.time_cost = 0
        pass

    def fuzz(self):
        """Return fuzz input"""
        return ""

    # @timeout(5)
    def run(self, runner=Runner()):
        """Run `runner` with fuzz input"""
        if Actual_Time:
            start = time.time() * 1000000
            res = runner.run(self.fuzz())
            end = time.time() * 1000000
            self.time_cost = end - start
            return res
        else:
            res = runner.run(self.fuzz())
            return res

    def runs(self, runner=PrintRunner(), trials=10):
        """Run `runner` with fuzz input, `trials` times"""
        # Note: the list comprehension below does not invoke self.run() for subclasses
        # return [self.run(runner) for i in range(trials)]
        outcomes = []
        for i in range(trials):
            outcomes.append(self.run(runner))
        return outcomes

class MutationFuzzer(Fuzzer):
    def __init__(self, seed, min_mutations=2, max_mutations=10):
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        ''' List of all mutations. If you want to add/remove mutations, do it here! '''
        # globals
        self.MAX8  = 0xff
        self.MAX16 = 0xffff
        self.MAX32 = 0xffffffff

        # Format :
        # - 'value' and 'size' are self explanatory
        # - 'type' is either 'replace' or 'insert'
        #   - replace: overwrite the bytes at a specific offset with the new bytes
        #     - aka: AAAAAAAAAA -> AAAABBBBAA
        #   - insert: insert the bytes at a specific offset with the new bytes, shifting the rest of the bytes down
        #     - aka: AAAAAAAAAA -> AAAABBBBAAAAAA
        self.values_8bit  = [{'value':0x00,       'type':'replace', 'size':1}, {'value':0x01,    'type':'replace', 'size':1}, {'value':self.MAX8/2-16,  'type':'replace', 'size':1},
                        {'value':self.MAX8/2-1,   'type':'replace', 'size':1}, {'value':self.MAX8/2,  'type':'replace', 'size':1}, {'value':self.MAX8/2+1,   'type':'replace', 'size':1},
                        {'value':self.MAX8/2+16,  'type':'replace', 'size':1}, {'value':self.MAX8-1,  'type':'replace', 'size':1}, {'value':self.MAX8,       'type':'replace', 'size':1} ]

        self.values_16bit  = [{'value':0x00,      'type':'replace', 'size':2}, {'value':0x01,    'type':'replace', 'size':2}, {'value':self.MAX16/2-16, 'type':'replace', 'size':2},
                        {'value':self.MAX16/2-1,  'type':'replace', 'size':2}, {'value':self.MAX16/2, 'type':'replace', 'size':2}, {'value':self.MAX16/2+1,  'type':'replace', 'size':2},
                        {'value':self.MAX16/2+16, 'type':'replace', 'size':2}, {'value':self.MAX16-1, 'type':'replace', 'size':2}, {'value':self.MAX16,      'type':'replace', 'size':2} ]

        self.values_32bit  = [{'value':0x00,       'type':'replace', 'size':4}, {'value':0x01,    'type':'replace', 'size':4}, {'value':self.MAX32/2-16, 'type':'replace', 'size':4},
                        {'value':self.MAX32/2-1,  'type':'replace', 'size':4}, {'value':self.MAX32/2, 'type':'replace', 'size':4}, {'value':self.MAX32/2+1,  'type':'replace', 'size':4},
                        {'value':self.MAX32/2+16, 'type':'replace', 'size':4}, {'value':self.MAX32-1, 'type':'replace', 'size':4}, {'value':self.MAX32,      'type':'replace', 'size':4} ]

        self.values_strings = [{'value':list("B"*100),  'type':'insert', 'size':100}, \
                          {'value':list("B"*1000), 'type':'insert', 'size':1000}, \
                          {'value':list("B"*10000),'type':'insert', 'size':10000}, \
                          {'value':list("%s"*10),  'type':'insert', 'size':10}, \
                          {'value':list("%s"*100), 'type':'insert', 'size':100}]
        self.reset()

    def reset(self):
        self.population = self.seed
        self.seed_index = 0

    def insert_random_character(self, s):
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        if Only_Num:
            random_character = chr(random.randint(48, 57))
        else:
            random_character = chr(random.randint(33, 127))
        # print("Inserting", repr(random_character), "at", pos)
        return s[:pos] + random_character + s[pos:]

    def delete_random_character(self, s):
        """Returns s with a random character deleted"""
        if s == "":
            return s
        pos = random.randint(0, len(s) - 1)
        # print("Deleting", repr(s[pos]), "at", pos)
        return s[:pos] + s[pos + 1:]

    def flip_random_character(self, s):
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return s

        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        if Only_Num:
            new_c = chr(random.randint(48, 57))
        elif ord(c) <= 39:
            new_c = chr(random.randint(48, 57))
        else:
            bit = 1 << random.randint(0, 6)
            new_c = chr(ord(c) ^ bit)
        # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
        return s[:pos] + new_c + s[pos + 1:]

    def rnd_subset_reorder(self, s):
        """randomly change the order of a subset of the input bytes"""
        if s == "":
            return s
        pos = random.randint(0, len(s) - 1)
        range = random.randint(pos, len(s) - 1)
        substr = s[pos:range]
        substr_rev = substr[::-1]
        return s[:pos] + substr_rev + s[range + 1:]

    def flip_digit_character(self, s):
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return s
        poss_chars_indx = []
        indx = 0
        for char in s:
            if ord(char) >= 48 and ord(char) <= 57:
                poss_chars_indx.append(indx)
            indx = indx + 1
        pos = random.choice(poss_chars_indx)
        c = s[pos]
        if Only_Num:
            new_c = chr(random.randint(48, 57))
        else:
            bit = 1 << random.randint(0, 6)
            new_c = chr(ord(c) ^ bit)
        # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
        return s[:pos] + new_c + s[pos + 1:]

    def SwapByte(self,data):
        fuzzed = ''
        if len(data) < 2:
            return data

        rnd1 = random.randint(0, len(data) - 1)
        if rnd1 >= 1:
            rnd2 = random.randint(0, rnd1 - 1)
        elif rnd1 + 1 <= len(data) - 1:
            rnd2 = random.randint(rnd1 + 1, len(data) - 1)

        min_rnd = min(rnd1, rnd2)
        max_rnd = max(rnd1, rnd2)

        byte1 = data[min_rnd]
        byte2 = data[max_rnd]

        fuzzed = data[:min_rnd]
        fuzzed += byte2
        fuzzed += data[min_rnd + 1:max_rnd]
        fuzzed += byte1
        fuzzed += data[max_rnd + 1:]

        return fuzzed

    def SwapWord(self,data):
        fuzzed = ''
        if len(data) < 4:
            return data

        rnd1 = random.randint(0, len(data) - 2)

        if rnd1 >= 2:
            rnd2 = random.randint(0, rnd1 - 2)
        elif rnd1 + 2 <= len(data) - 2:
            rnd2 = random.randint(rnd1 + 2, len(data) - 2)
        else:
            return data

        min_rnd = min(rnd1, rnd2)
        max_rnd = max(rnd1, rnd2)

        word1 = data[min_rnd:min_rnd + 2]

        word2 = data[max_rnd:max_rnd + 2]

        fuzzed = data[:min_rnd]
        fuzzed += word1
        fuzzed += data[min_rnd + 2:max_rnd]
        fuzzed += word2
        fuzzed += data[max_rnd + 2:]

        return fuzzed

    def  ByteNullifier(self, data):
        fuzzed = ''
        if len(data) == 0:
            return data
        index = random.randint(0, len(data) - 1)

        fuzzed = '%s\x00%s' % (data[:index], data[index + 1:])
        return fuzzed

    def IncreaseByOneMutator(self, data, howmany=1):
        if len(data) == 0:
            return data
#        howmany = random.choice(range(1,4))
        if len(data) < howmany:
            howmany = random.randint(1, len(data))

        fuzzed = data

        for _ in xrange(howmany):
            index = random.randint(0, len(data) - 1)
            if ord(data[index]) != 0xFF:
                fuzzed = '%s%c%s' % (
                        data[:index],
                        ord(data[index]) + 1,
                        data[index + 1:]
                    )
            else:
                fuzzed = '%s\x00%s' % (
                        data[:index],
                        data[index + 1:]
                        )

            data = fuzzed

        return fuzzed

    def DecreaseByOneMutator(self, data, howmany=1):
        if len(data) == 0:
            return data
#        howmany = random.choice(range(1,4))
        if len(data) < howmany:
            howmany = random.randint(0, len(data) - 1)

        fuzzed = data
        for _ in xrange(howmany):
            index = random.randint(0, len(data) - 1)
            if ord(data[index]) != 0:
                fuzzed = '%s%c%s' % (
                        data[:index],
                        ord(data[index]) - 1,
                        data[index + 1:]
                    )
            else:
                fuzzed = '%s\xFF%s' % (
                    data[:index],
                    data[index + 1:]
                )
            data = fuzzed
        return fuzzed

    def ProgressiveIncreaseMutator(self, data, howmany=8):
        if len(data) < 2:
            return data
        howmany = random.choice(range(2,len(data)+1))
        index = random.randint(0, len(data) - howmany)
        buf = ''
        fuzzed = ''

        for curr in xrange(index, index + howmany):
            addend = 1
            if addend + ord(data[curr]) > 0xFF:
                addend -= 0xFF
            buf += chr(ord(data[curr]) + addend)

        fuzzed = '%s%s%s' % (data[:index], buf, data[index + howmany:])
        return fuzzed

    def ProgressiveDecreaseMutator(self, data, howmany=8):
        if len(data) < 2:
            return data
        howmany = random.choice(range(2,len(data)+1))
        index = random.randint(0, len(data) - howmany)
        buf = ''
        fuzzed = ''

        for curr in xrange(index, index + howmany):
            dec = 1
            if ord(data[curr]) >= dec:
                buf += chr(ord(data[curr]) - dec)
            else:
                buf += chr(dec - ord(data[curr]))

        fuzzed = '%s%s%s' % (data[:index], buf, data[index + howmany:])
        return fuzzed

    def SetHighBitFromByte(self, data):
        fuzzed = ''

        if len(data) > 0:
            index = random.randint(0, len(data) - 1)
            byte = ord(data[index])
            byte |= 0x80
            fuzzed = data[:index]
            fuzzed += chr(byte)
            fuzzed += data[index + 1:]

        return fuzzed

    def DuplicateByte(self, data, howmany=1):
        fuzzed = ''
        if len(data) < 1:
            return data

        for _ in xrange(howmany):
            index = random.randint(0, len(data) - 1)
            byte = data[index]
            fuzzed = data[:index]
            fuzzed += byte
            fuzzed += data[index:]

        return fuzzed

    def crossover_2(self, s):
        if len(self.population) == 0:
            return s;
        s1 = random.choice(self.population)
        if len(s1) <= 1 or len(s) <= 1:
            return s;
        # print("original string is: " + s)
        pos = random.randint(0, len(s) - 1)
        pos1 = random.randint(0, len(s1) - 1)
        father, mother = s[:pos], s1[pos1+1:]
        index1 = random.randint(1, len(s) - 1)
        index2 = random.randint(1, len(s1) - 1)
        if index1 > index2: index1, index2 = index2, index1
        child1 = father[:index1] + mother[index1:index2] + father[index2:]
        child2 = mother[:index1] + father[index1:index2] + mother[index2:]
        # print("crossover string is: " + child1 + " " + child2)
        return child1 + child2

    def mutate(self, s):
        """Return s with a random mutation applied"""
        mutators = [
            self.delete_random_character,
            self.insert_random_character,
            self.flip_random_character,
            self.rnd_subset_reorder,
            self.SwapByte,
            # self.flip_digit_character
            # self.SwapWord
            # self.IncreaseByOneMutator,
            # self.DecreaseByOneMutator,
            # self.ByteNullifier,
            # self.ProgressiveIncreaseMutator,
            # self.ProgressiveDecreaseMutator,
            # self.SetHighBitFromByte,
            # self.DuplicateByte
            ]
        mutator = random.choice(mutators)
        index_s = mutators.index(mutator)
        # specific for input with array separated with space
        s = " ".join(mutator(s).split())
        return s, index_s

    def action_RL(self, s, a):
        """Return s with an action from RL"""
        mutators = [
            self.delete_random_character,
            self.insert_random_character,
            self.flip_random_character,
            self.rnd_subset_reorder,
            self.crossover_2,
            self.SwapByte,
            self.SwapWord,
            self.IncreaseByOneMutator,
            self.DecreaseByOneMutator,
#            self.ByteNullifier,
            self.ProgressiveIncreaseMutator,
            self.ProgressiveDecreaseMutator,
            self.SetHighBitFromByte
#            self.DuplicateByte
        ]
        if a == 4:
            s, _ = self.mutate(s)
        mutator = mutators[a]
        # specific for input with array separated with space
        s = " ".join(mutator(s).split())
        return s

    def create_candidate(self, mutate = True, cur_act = 0, e = 0.1, m_p = 0.1):
        a_index = -1
        if mutate:
            sum_costs = np.sum(self.cost)
            prob = [float(x/sum_costs) for x in self.cost]
            if random.random() < e:
                max_index = np.argmax(self.cost)
                candidate = self.population[max_index]
            elif np.sum(prob) > 0.999:
                candidate = np.random.choice(self.population,p=prob)
            else:
                candidate = random.choice(self.population)
            trials = random.randint(self.min_mutations, self.max_mutations)
            for i in range(trials):
                candidate, a_index = self.mutate(candidate)
            if random.random() < m_p:       # with this probability, do crossover
                candidate = self.crossover_2(candidate)
        else:
            candidate = self.inp
            if random.random() < e:       # with small probability do mutations!
                trials = random.randint(self.min_mutations, self.max_mutations)
                for i in range(trials):
                    candidate, a_index = self.mutate(candidate)
                if random.random() < m_p:       # with this probability, do crossover
                    candidate = self.crossover_2(candidate)
            else:
                candidate = self.action_RL(candidate, cur_act)
                a_index = cur_act
        return candidate, a_index

    def fuzz(self, mutate = True, cur_act = 0, e_prob = 0.01):
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp, self.action = self.create_candidate(mutate, cur_act, e_prob)
        # print("current input is: " + self.inp)
        return self.inp

class FunctionRunner(Runner):
    def __init__(self, function):
        """Initialize.  `function` is a function to be executed"""
        self.function = function


    def run_function(self, inp):
        return self.function(inp)

    def run(self, inp):
        try:
            result = self.run_function(inp)
            outcome = self.PASS
        except Exception:
            result = None
            outcome = self.FAIL

        return result, outcome

class FunctionCoverageRunner(FunctionRunner):
    def run_function(self, inp):
        with Coverage() as cov:
            try:
                result = super(FunctionCoverageRunner,self).run_function(inp)
            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc

        self._coverage = cov.coverage()
        return result

    def coverage(self):
        return self._coverage

class MutationCoverageFuzzer(MutationFuzzer):
    def reset(self):
        super(MutationCoverageFuzzer,self).reset()
        self.coverages_seen = []
        self.population = []
        self.cost = []
        self.cost_path = []
        self.new_coverage = 0
        self.action = -1
        self.inp = ""
        self.num_inp = 0
        self.time_in_ext_analysis = 0
        self.count_extreme_dist = 0
        self.prob = 0


    def run(self, runner):
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        try:
            result, outcome = super(MutationCoverageFuzzer,self).run(runner)
        except TimeoutError as error:
            print("Caght an error!")
            return ""
        key_path = runner.coverage()[0]
        if Actual_Time:
            val_cost = self.time_cost
            path_cost = runner.coverage()[1]

        else:
            val_cost = runner.coverage()[1]
            path_cost = 0

        # if key_path in self.coverages_seen:
        #     return result
            
        self.new_coverage = val_cost
        self.num_inp += 1
        inp_num_args = self.inp.split(" ")

        if self.num_inp <= ITER_to_Model and len(inp_num_args) <= MAX_SIZE:
            self.population.append(self.inp)
            self.coverages_seen.append(key_path)
            self.cost.append(val_cost)
            self.cost_path.append(path_cost)
        elif len(inp_num_args) <= MAX_SIZE:
            cost_avg = np.mean(self.cost)
            cost_std = np.std(self.cost)
            threshold = cost_avg + 2.0 * cost_std
            extr_costs = list(filter(lambda x: x >= threshold, self.cost))
            if val_cost >= threshold and val_cost <=  cost_avg + 3.0 * cost_std:
                self.population.append(self.inp)
                self.coverages_seen.append(key_path)
                self.cost.append(val_cost)
                self.cost_path.append(path_cost)
            elif val_cost > cost_avg + 3.0 * cost_std and len(extr_costs) > 30:
                extr_avg = np.mean(extr_costs)
                extr_std = np.std(extr_costs)
                self.prob = norm.cdf(val_cost, loc=extr_avg, scale=extr_std)
                if self.prob <= 0.95:
                    self.count_extreme_dist = self.time_in_ext_analysis + 1
                    self.population.append(self.inp)
                    self.coverages_seen.append(key_path)
                    self.cost.append(val_cost)
                self.time_in_ext_analysis += 1
        # print("Time in the analysis: " + str(self.time_in_analysis))
        return result

def population_coverage(population, function):
    cumulative_coverage = []
    prev_cov = 0
    all_coverage = []

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except:
                pass
        all_coverage.append(cov.coverage())
        cumulative_coverage.append(cov.coverage() - prev_cov)
        prev_cov = cov.coverage()

    return all_coverage, cumulative_coverage

@timeout(60)
def run_driver(inp_program_instr, mutation_fuzzer):
    for i in range(NUM_ITER):
        mutation_fuzzer.runs(inp_program_instr, trials=TRIASL_EACH_ITER)
        for j in range(len(mutation_fuzzer.coverages_seen)):
            print("The path key is: " + str(mutation_fuzzer.coverages_seen[j]))
            print("step: " + str(i+1))
            print(mutation_fuzzer.cost[j])
            print(mutation_fuzzer.population[j])
            print(mutation_fuzzer.cost_path[j])

    # print("Best input and coverage overall!")
    # max_int = mutation_fuzzer.coverages_seen.index(max(mutation_fuzzer.coverages_seen))
    # print(max(mutation_fuzzer.coverages_seen))
    # print(mutation_fuzzer.population[max_int])
    # store the results!
    # based on the length of inputs!
    return mutation_fuzzer

if __name__ == "__main__":
    # Every algorithm except Booyer Moore and prime_MST 
    seed_inputs = ["1 3","12 9 10 5","17 15 20"]
    start_time = time.time()
    # for Boyer_Moore
    # seed_inputs = ["123-ABC", "123-111", "ABAA-BA", "123456-456"]
    # for prim MST
    # seed_inputs = ["0 1 3 1 2 2 2 0 1","0 1 2 1 2 3 2 3 6","0 1 3 1 3 5 2 3 4 1 2 10"]
    #seed_inputs = ["0.11 3 4 10","-1.16 5 3 50","2.12 7 4 101"]
    # seed_inputs = ["50 1000 50 1","150 1000 60 0","250 1000 70 0"]
    #seed_inputs = ["400 50 10 0","430 50 10 0","100 50 10 0","150 50 10 0","180 50 10 0","210 50 10 0","240 50 10 0","275 50 10 0","300 50 10 0","330 50 10 0","350 50 10 0","450 50 10 0","500 50 10 0","520 50 10 0","530 50 10 0","550 50 10 0","580 50 10 0","610 50 10 0","650 50 10 0","700 50 10 0","719 50 10 0","745 50 10 0","800 50 10 0","820 50 10 0","850 50 10 0","870 50 10 0","900 50 10 0","920 50 10 0","950 50 10 0","970 50 10 0","990 50 10 0","1000 50 10 0"]
    # seed_inputs = ["1000 200 10.0 10 1 1 0","2000 200 1.0 10 1 1 1","5000 200 0.1 10 1 1 0"]
    # seed_inputs = ["10000 10 2 5 1 2 1 1 0.0001 1.0 0 1.0 100 0"]
    # seed_inputs = ["1000 10 2 2 0 1 0 1 0 0 0.01 0.0"]
    # seed_inputs = ["50 2 0 2 0 0 10 0.1 0 3 0.01 0 2.0 1.0 1"]
    inp_program_instr = FunctionCoverageRunner(input_program)
    mutation_fuzzer = MutationCoverageFuzzer(seed=seed_inputs, min_mutations = 1, max_mutations = 5)
    f1 = open("complexity_driver_EVT_" + str(input_program).split(" ")[1] + "_" + str(start_time).split(".")[0] + ".csv", "w")
    try:
        run_driver(inp_program_instr, mutation_fuzzer)
    except TimeoutError as error:
        for i in range(len(mutation_fuzzer.coverages_seen)):
            inp_pop = mutation_fuzzer.population[i]
            c1 = mutation_fuzzer.cost[i]
            c2 = mutation_fuzzer.cost_path[i]
            key = mutation_fuzzer.coverages_seen[i]
            f1.write(str(inp_pop) + "," + str(c1) + "," + str(c2) + "," + str(key) +"\n")
        f1.close()
    for i in range(len(mutation_fuzzer.coverages_seen)):
        inp_pop = mutation_fuzzer.population[i]
        c1 = mutation_fuzzer.cost[i]
        c2 = mutation_fuzzer.cost_path[i]
        key = mutation_fuzzer.coverages_seen[i]
        f1.write(str(inp_pop) + "," + str(c1) + "," + str(c2) + "," + str(key) +"\n")
    f1.close()
