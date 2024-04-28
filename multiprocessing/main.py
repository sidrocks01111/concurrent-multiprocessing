from multiprocessing import Process, Queue, Pool, cpu_count
from functools import partial

from threading import Thread
import time

# def check_value_in_list(x, i, total_num_processes, queue):
#     max_number_to_check_to = 10**8
#     lower = int(i * max_number_to_check_to / total_num_processes)
#     upper = int((i + 1) * max_number_to_check_to / total_num_processes)
#     number_of_hits = 0
#     for i in range(lower, upper):
#         if i in x:
#             number_of_hits += 1
#     queue.put((lower, upper, number_of_hits))

# value of x is changing so it is at last
# def square(y, addition_component, x):
#     return x ** 2

def check_number_of_valuess_in_range(comp_list, lower, upper):
    number_of_hits = 0
    for i in range(lower, upper):
        if i in comp_list:
            number_of_hits += 1
    return number_of_hits

if __name__ == '__main__':

    num_processes = 2
    comparison_list = [0, 1, 2, 3]
    lower_and_upper_bounds = [(0, 25*10**6), (25*10*6, 50*10**6), (50*10**6, 75*10*6), (75*10*6, 10**8)]

    start_time = time.time()
    num_of_cpus_available = max(1, cpu_count() - 6)
    print('num of cpus being used', num_of_cpus_available)
    
    # partial function to pass in additional parameters 
    # partial_func = partial(square, power, addition_component)
    # with Pool(num_of_cpus_available) as mp_pool:
    #    result = mp_pool.map(partial_func, comparison_list)
    
    prepared_list = []
    for i in range(len(lower_and_upper_bounds)):
        prepared_list.append((comparison_list, *lower_and_upper_bounds[i]))
    print('input list', prepared_list)
    
    
    with Pool(num_of_cpus_available) as mp_pool:
        result = mp_pool.starmap(check_number_of_valuess_in_range, prepared_list) #[square(1, 4), square(2, 5), square(3, 6)]
        
    print(result)

    print('Everything took:', time.time() - start_time, 'second')