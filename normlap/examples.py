from multiprocessing.connection import Pipe
from Formatter import Formatter
from RandomSubnetwork import RandomSubnetwork
from RandomNetwork import RandomNetwork
from Pipeline import Pipeline
import matplotlib.pyplot as plt
import numpy as np

elist1 = [(1, 2), (2, 3), (3, 5)]  # an example network1
elist2 = [(2, 3), (4, 5), (1, 2), (2, 4)]  # an example network2
elist0 = elist1 + elist2 + [(2, 5), (1, 5), (3, 4), (1, 6), (1, 4)]


# Test Formatter
dict1 = Formatter.edgelist_to_neighborhood(elist1)
dict2 = Formatter.edgelist_to_neighborhood(elist2)
dict0 = Formatter.edgelist_to_neighborhood(elist0)
print("Finished test Formatter")
print("dict1: ", dict1)

# print all attribute of RandomSubnetwork
print("RandomSubnetwork attributes: ", dir(RandomSubnetwork))

# Test RandomSubnetwork optimize alphas with stopping criteria
alphas, alphas_history, cur_iter = RandomSubnetwork.optimize_alpha_with_stop(
    dict0, dict2, max_iters=10000, stopping_criterion=10e-5)
print("-"*40)
print("Finished test RandomSubnetwork optimize alphas with stopping criteria")
print("alphas: ", alphas)
print("alphas_history: ", alphas_history[-3:])
print("cur_iter: ", cur_iter)

# Test RandomSubnetwork optimize pos
pos_mean, pos_sigma, cur_iter = RandomSubnetwork.optimize_pos(
    elist1, elist2, iters_start=1000, pos_change_limit=1, iter_spacing=100, max_iterations=2000)
print("-"*40)
print("Finished test RandomSubnetwork optimize pos")
print("pos_mean: ", pos_mean)
print("pos_sigma: ", pos_sigma)
print("cur_iter: ", cur_iter)


# Test RandomNetwork optimize alpha with stopping criteria
alphas, alphas_history, cur_iter = RandomNetwork.optimize_alpha_with_stop(
    dict1, max_iters=10000, stopping_criterion=10e-6)
print("-"*40)
print("Finished test RandomNetwork optimize alpha with stopping criteria")
print("alphas: ", alphas)
print("alphas_history: ", alphas_history[-3:])
print("cur_iter: ", cur_iter)

# Test RandomNetwork optimize neg
neg_mean, neg_sigma, cur_iter = RandomNetwork.optimize_neg(
    elist1, elist2, iters_start=100, neg_change_limit=0.1, iter_spacing=100, max_iterations=2000)
print("-"*40)
print("Finished test RandomNetwork optimize neg")
print("neg_mean: ", neg_mean)
print("neg_sigma: ", neg_sigma)
print("cur_iter: ", cur_iter)

# Test Pipeline
pipe = Pipeline(elist1, elist2)
print("-"*40)
labels, results = pipe.show_results(printOn=True)

# Test customized Pipeline
pipe = Pipeline(elist1, elist2)
pos_mean, pos_sigma = pipe.get_pos_benchmark(
    iters_start=100, pos_change_limit=1.0, iter_spacing=100, max_iterations=2000)
neg_mean, neg_sigma = pipe.get_neg_benchmark(
    iters_start=100, neg_change_limit=0.1, iter_spacing=100, max_iterations=2000)
print("-"*40)
labels, results = pipe.show_results(printOn=True)

# Test get neg instance
pipe = Pipeline(elist1, elist2)
neg_instance1 = pipe.get_neg_instance(idx=0)
print("-"*40)
print(neg_instance1)
