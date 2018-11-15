num_test_cases = 5000
stop_brute_force_at_test_case = 10
upper_bound_for_random = 100 # Used for t and w. Cost overflow for high values hence 100

assert stop_brute_force_at_test_case <= num_test_cases

import time
import random
random.seed(1)
from itertools import permutations
import matplotlib.pyplot as plt

def random_init_dataset(num_jobs):
	'''
	Return list of jobs. Each job is a dictionary with its job number, time and weight.
	'''
	job_set = []
	for i in range(num_jobs):
		time = random.randint(1, upper_bound_for_random)
		weight = random.randint(1, upper_bound_for_random)
		job_set.append({'job_no': i, 'time': time, 'weight': weight})
	return job_set

def greedy_sequencing(job_set):
	'''
	Greedy solution that returns a sequence in which jobs should we executed with its associated cost.
	'''
	greedy_set = []
	for job in job_set:
		greedy_set.append({'job_no': job['job_no'], 'ratio': (job['time'] / job['weight'])}) # Ratio of time / weight
	greedy_set = sorted(greedy_set, key = lambda k: k['ratio']) # Sorting in ascending order
	sequence = []
	cost = 0
	C_i = 0
	for job in greedy_set:
		sequence.append(job['job_no'])
		C_i += job_set[job['job_no']]['time'] # Since finish time for the job is sum of its start time (previous job's finish time) and its execution time
		W_i = job_set[job['job_no']]['weight']
		cost += (C_i * W_i)
	return sequence, cost

def brute_force_sequencing(job_set):
	'''
	Brute force solution that returns a sequence in which jobs should we executed with its associated cost.
	'''
	job_number_list = [job['job_no'] for job in job_set]
	min_cost = 1e10
	# Returns all permutations of size len(job_number_list)
	for sequence in permutations(job_number_list, len(job_number_list)):
		C_i = 0
		cost = 0
		for job_no in sequence:
			C_i += job_set[job_no]['time']
			W_i = job_set[job_no]['weight']
			cost += (C_i * W_i)
		if(cost < min_cost):
			optimal_sequence = sequence
			min_cost = cost
	return optimal_sequence, min_cost


greedy_plot = []
bf_plot = []
for iteration in range(1, num_test_cases + 1):

	print('-' * 20)
	print('ITERATION:', iteration)

	num_jobs = iteration
	job_set = random_init_dataset(num_jobs)
	# print('JOBS:', job_set)

	since = time.time()
	sequence, cost = greedy_sequencing(job_set)
	elapsed = time.time() - since
	greedy_plot.append(elapsed)

	if(iteration <= stop_brute_force_at_test_case):
		print('GREEDY SEQUENCE:', sequence, 'COST:', cost, 'TIME:', elapsed)
		since_bf = time.time()
		optimal_sequence, min_cost = brute_force_sequencing(job_set)
		elapsed_bf = time.time() - since_bf
		print('BF SEQUENCE:', optimal_sequence, 'COST:', min_cost, 'TIME:', elapsed_bf)
		bf_plot.append(elapsed_bf)
	
	else:
		print('GREEDY COST:', cost, 'TIME:', elapsed)
		pass


# Plotting code
plt.plot(list(range(1, len(greedy_plot) + 1)), greedy_plot, label = 'Greedy')
plt.plot(list(range(1, len(bf_plot) + 1)), bf_plot, label = 'Brute force')
plt.title('Brute force v/s Greedy approach for \'Weighted job sequencing\'')
plt.xlabel('Number of jobs in each test case')
plt.ylabel('Time (s)')
plt.legend(loc = 'upper right')
plt.yscale('log')
plt.xscale('log')
plt.show()