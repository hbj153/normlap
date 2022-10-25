from normlap.Pipeline import Pipeline

elist1 = [(1, 2), (2, 3), (3, 5)]  # an example network1
elist2 = [(2, 3), (4, 5), (1, 2), (2, 4)]  # an example network2
elist0 = elist1 + elist2 + [(2, 5), (1, 5), (3, 4), (1, 6), (1, 4)]

# Test customized Pipeline
pipe = Pipeline(elist1, elist2)
pos_mean, pos_sigma = pipe.get_pos_benchmark(
    iters_start=100, pos_change_limit=1.0, iter_spacing=100, max_iterations=2000)
neg_mean, neg_sigma = pipe.get_neg_benchmark(
    iters_start=100, neg_change_limit=0.1, iter_spacing=100, max_iterations=2000)
print("-"*40)
labels, results = pipe.show_results(printOn=True)
