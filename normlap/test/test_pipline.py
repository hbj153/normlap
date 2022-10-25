# import all class from normlap
# current working dictionary: py_normlap



elist1 = [(1, 2), (2, 3), (3, 5)]
elist2 = [(2, 3), (4, 5), (1, 2), (2, 4)]
elist0 = elist1 + elist2 + [(2, 5), (1, 5), (3, 4), (1, 6), (1, 4)]

# Test Formatter
dict1 = Formatter.edgelist_to_neighborhood(elist1)
dict2 = Formatter.edgelist_to_neighborhood(elist2)
dict0 = Formatter.edgelist_to_neighborhood(elist0)
print("Finished test Formatter")
print("dict1: ", dict1)

# print all attribute of RandomSubnetwork
print("RandomSubnetwork attributes: ", dir(RandomSubnetwork))

# Test RandomSubnetwork optimize pos
pos_mean, pos_sigma, cur_iter = RandomSubnetwork.optimize_pos(
    elist1, elist2, iters_start=1000, pos_change_limit=1, iter_spacing=100, max_iterations=2000)
print("Finished test RandomSubnetwork optimize pos")
print("pos_mean: ", pos_mean)
print("pos_sigma: ", pos_sigma)
print("cur_iter: ", cur_iter)
