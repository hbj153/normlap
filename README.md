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

