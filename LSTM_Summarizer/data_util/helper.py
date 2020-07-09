
from functools import partial
from multiprocessing import cpu_count, Pool


# Helper function for parallel processing
def parallel_map(lst, func):
    # Create a thread pool
    pool = Pool(cpu_count())
    # Run the function and concatenate the result
    lst = pool.map(func, lst)
    # Clean up
    pool.close()
    pool.join()
    return lst