from cython_code import my_array
from array import array as another_array
import time

a = my_array.array("i", [1, 2, 1])


a.append(2000)

print(a)