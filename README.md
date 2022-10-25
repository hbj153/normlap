# normlap
---
Compares the observed overlap between networks with the negative and positive benchmarks. It also provides the functions to:

- randomize the network while preserving the degree sequence
- randomly select a subnetwork from the given pool network according to the degree sequence of the input network.

The randomization is based on the maximum entropy framework.

## Get started
If you have two networks represented in the edge list format and `normlap` package installed, you already have everything you need to start using normlap.

### Quick start

To use the default settings of generating positive benchmark, negative benchmark and calculate the normlap score, run as follows:

```python
from normlap import Pipeline
elist1 = [(1, 2), (2, 3), (3, 5)] # an example network1
elist2 = [(2, 3), (4, 5), (1, 2), (2, 4)] # an example network2
pipe = Pipeline(elist1,elist2)
labels,results = pipe.show_results(printOn=True)

```

In addition to saving the results to the given variables, the results will be printed out with `printOn=True` option as below:

```html
The get_pos_benchmark function has not been called yet. The results will be calculated based on default parameters.
The get_neg_benchmark function has not been called yet. The results will be calculated based on default parameters.
Observed overlap:  2.00
Neg_mean:  1.33
Neg_sigma:  0.67
Neg_p:  0.16
Pos_mean:  2.00
Pos_sigma:  0.06
Pos_p:  0.50
Normlap:  1.00
Normlap_sigma:  0.09
```

The default setting stop iterating the value of alphas when the absolute change of pos_mean(neg_mean) < 1.

To customize the stopping criterion, use the following:

```python
pipe = Pipeline(elist1, elist2)
pos_mean, pos_sigma = pipe.get_pos_benchmark(
    iters_start=100, pos_change_limit=1.0, iter_spacing=100, max_iterations=2000)
neg_mean, neg_sigma = pipe.get_neg_benchmark(
    iters_start=100, neg_change_limit=0.1, iter_spacing=100, max_iterations=2000)
labels, results = pipe.show_results(printOn=True)
```

This allows you to customize the details of iterations, the results are as follows:

```text
Observed overlap:  2.00
Neg_mean:  1.33
Neg_sigma:  0.67
Neg_p:  0.16
Pos_mean:  2.00
Pos_sigma:  0.20
Pos_p:  0.50
Normlap:  1.00
Normlap_sigma:  0.29
```

## Example Use

### 1. Generate randomized network

The `Pipeline.get_neg_instance`  fucntion allows you to get a randomized version of the given network. The randomization preserves the degree sequence on average based on the maximum entropy framework.

```python
# generate randomized network instance
from normlap import Pipeline
elist1 = [(1,2),(2,3),(3,5)]
elist2 = [(2,3),(4,5),(1,2),(2,4)]
pipe = Pipeline(elist1,elist2)
neg_instance1 = pipe.get_neg_instance(idx=0)
print(neg_instance1)
neg_instance2 = pipe.get_neg_instance(idx=1)
print(neg_instance2)
```

```html
[(1, 3), (2, 3)]
[(1, 2), (2, 3), (2, 4), (2, 5)]
```



### 2. Generate randomized subnetwork from the given union

The `Pipeline.get_pos_instance` function allows you to generate a randomized subnetwork from the pool, while preserving the degree sequence on average. If the pool is not given, the default is to use the union of the two input networks. For broader application, normlap package provides the option to generate random subnetwork instance from an **customized pool** as below.

```python
from normlap import Pipeline
elist1 = [(1,2),(2,3),(3,5)]
elist2 = [(2,3),(4,5),(1,2),(2,4)]
elist0 = elist1 + elist2 + [(2,5),(1,5),(3,4),(1,6),(1,4)]

pipe = Pipeline(elist1, elist2, poollist=elist0)
pos_instance1 = pipe.get_pos_instance(idx=0)
print(pos_instance1)
pos_instance2 = pipe.get_pos_instance(idx=1)
print(pos_instance2)
```

```html
[(1, 2), (2, 3), (3, 5)]
[(2, 3), (4, 5), (2, 4), (2, 5)]
```



## Citing

