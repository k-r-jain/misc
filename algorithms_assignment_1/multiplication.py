from random import randint
from timeit import timeit
# from memory_profiler import profile
import matplotlib.pyplot as plt
from sys import getsizeof

def gen_rand_ints(digit_size = 8, list_size = 1000):
    '''Returns a list of m integers each of n digits where m = list_size and n = digit_size'''
    list_of_ints = []
    for i in range(list_size):
        digit = str(randint(1, 9)) # So that the most significant digit is not set to zero effectively making the result of size n - 1
        for j in range(1, digit_size):
            digit += str(randint(0, 9)) # String concatenation
        list_of_ints.append(int("".join(digit)))
    return list_of_ints

# @profile
def multiply(operand_a, operand_b):
    '''Returns an integer which is the product of two arguments passed. Works only for unsigned decimal numbers'''

    # Generating a fixed size matrix using python's multiplication operator (*)
    elementary_multiplication_matrix = [[0 for i in range(10)] for j in range(10)]
    for i in range(10):
        for j in range(10):
            elementary_multiplication_matrix[i][j] = i * j # To generate all 100 combinations of multiplications from 0x0 = 0 to 9x9 = 81

    # Convert the two integers into list and reverse them (for ease of calculation)
    a = list(map(int, list(str(operand_a))))[::-1]
    b = list(map(int, list(str(operand_b))))[::-1]
    result = 0
    # Cache is of size 10. It is used to store the result of operand_a * p where p is a single digit [0, 9]
    cache = [-1 for j in range(10)]
    cache[0] = 0 # Since operand_a * 0 = 0

    for b_index in range(len(b)): # Grab one digit at a time from the second operand
        if(cache[b[b_index]] == -1): # Set cache if unavailable to save time later on
            tmp_result = 0
            for a_index in range(len(a)): # Grad one digit at a time from the first operand
                # p * q (where p and q are both [0, 9]) is looked up in the elementary_multiplication_matrix. The number of the zeros appended depends on the position of digit with first operand
                # For example, if q is a digit in the tens' place in operand_a, one zero will be appended
                tmp_result += int(str(elementary_multiplication_matrix[b[b_index]][a[a_index]]) \
                                  + ''.join(['0' for i in range(a_index)]))
                
            cache[b[b_index]] = tmp_result # Save the result in cache

        result += int(str(cache[b[b_index]]) + ''.join(['0' for i in range(b_index)])) # Same drill of appending zeros as above but w.r.t. the second operand

    # Returning sum of sizes of all the variables in this function to analyze space complexity
    # Using this technique since various memory profilers indicated O(1) which is, obviously, incorrect
    total_size = getsizeof(elementary_multiplication_matrix) + getsizeof(cache) + getsizeof(result) + getsizeof(operand_a) + getsizeof(operand_b) + \
                    getsizeof(a) + getsizeof(b) + getsizeof(tmp_result)
    total_size /= (1024) # To return output in Kilobytes
    return result, total_size

def wrapper_multiply(): # Since timeit doesn't accept functions with parameters
    for i in range(number_of_observations):
        result, total_size = multiply(operand_a_list[i], operand_b_list[i])

    

if __name__ == "__main__":
    sizes = [4, 8, 16, 32, 64, 128, 256, 512]
    number_of_observations = 1000 # Number of random tests for each size
    time_list = []
    operand_a_list = []
    operand_b_list = []
    memory_list = []

    for size in sizes:
        operand_a_list = gen_rand_ints(digit_size = size, list_size = number_of_observations)
        operand_b_list = gen_rand_ints(digit_size = size, list_size = number_of_observations)
        time = timeit(wrapper_multiply, number = 1)

        avg_memory_used = 0
        # Running the same operations for the second time since timeit function dumps the multiply function's return values (which we need to calculate memory usage)
        for i in range(number_of_observations):
            result, total_size = multiply(operand_a_list[i], operand_b_list[i])
            avg_memory_used += total_size

        avg_memory_used /= number_of_observations
        print("For size", size, ", Time:", time, "Space:", avg_memory_used)
        time_list.append(time)
        memory_list.append(avg_memory_used)

    # Plotting results
    fig, ax = plt.subplots()
    ax.plot(sizes, time_list, color = 'b', label = "Time (in seconds)")
    ax.plot(sizes, memory_list, color = 'g', label = "Space (in Kilobytes)")
    ax.scatter(sizes, time_list, s = 35, c = 'b')
    ax.scatter(sizes, memory_list, s = 35, c = 'g')
    ax.legend(loc = 'upper left', shadow = True)
    plt.xlabel("Input size (n digits)")
    plt.ylabel("Cost")
    plt.title("Custom multiplication results")
    plt.show()