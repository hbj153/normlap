# import all class from normlap
# current working dictionary: py_normlap
from normlap import *


elist1 = [(1, 2), (2, 3), (3, 5)]
elist2 = [(2, 3), (4, 5), (1, 2), (2, 4)]
elist0 = elist1 + elist2 + [(2, 5), (1, 5), (3, 4), (1, 6), (1, 4)]

# Test Formatter
dict1 = Formatter.edgelist_to_neighborhood(elist1)
dict2 = Formatter.edgelist_to_neighborhood(elist2)
dict0 = Formatter.edgelist_to_neighborhood(elist0)
print("Finished test Formatter")
print("dict1: ", dict1)
