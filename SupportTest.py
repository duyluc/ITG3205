import time
from timeit import  default_timer as timer


previous = timer()
time.sleep(0.5)
print(timer() - previous)