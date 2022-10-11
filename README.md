# normlap
---
Comparing observed overlap between networks with the negative and positive benchmarks.

## Get started
If you have two networks represented in the edge list format, you already have everything you need to start using normalp:

```python
from normlap import Pipeline
elist1 = [(1,2),(2,3),(3,5)] # an example network1
elist2 = [(2,3),(4,5),(1,2)] # an example network2
pipe = Pipeline(elist1,elist2)
labels,results = pipe.show_results(printOn=True)

```

In addition to saving the results to the given variables, the results will be printed out with `printOn=True` option as below:

```html
Observed overlap:  2.00
Neg_mean:  1.50
Neg_sigma:  0.50
Neg_p:  0.16
Pos_mean:  2.00
Pos_sigma:  0.07
Pos_p:  0.50
Normlap:  1.00
Normlap_sigma:  0.14
```



## Example Use

### 1. Generate randomized network

The randomization in normlap are based on the maximum entropy framework.

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

The positive benchmark is built on selecting random subnetwork from the union of the two input networks. For broader application, normlap package provides function to generate random subnetwork instance from an **self-defined edge list pool**. If the pool is not given, the default is to use the union of the two input network.

```python
from normlap import Pipeline
elist1 = [(1,2),(2,3),(3,5)]
elist2 = [(2,3),(4,5),(1,2),(2,4)]
elist0 = elist1 + elist2 + [(2,5),(1,5),(3,4),(1,6),(1,4)]

pipe = Pipeline(elist1,elist2,elist0)
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

