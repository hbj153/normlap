# import pandas as pd
# from Formatter import Formatter
# from RandomSubnetwork import RandomSubnetwork
# from Pipeline import Pipeline

elist1 = [(1,2),(2,3),(3,5)]
elist2 = [(2,3),(4,5),(1,2)]
elist0 = list(set(elist1).union(elist2))
# dict1 = Formatter.edgelist_to_neighborhood(elist1)
# dict2 = Formatter.edgelist_to_neighborhood(elist2)

# # # Test RandomSubnetwork
# # alphas,alpha_probe = RandomSubnetwork.optimize_alpha(dict1,dict2,iters=1000)
# # print(alphas)
# # probs = RandomSubnetwork.cal_probability(elist0,elist1,alphas)
# # print(probs)
# # Gsample = RandomSubnetwork.construct_sample_network(probs)
# # print(Gsample)

# # def test(idx: int=0):
# #     print(idx)

# # print(type(elist0))

# # Test Pipeline
# pipe = Pipeline(elist1,elist2)
# sample_network = pipe.get_pos_instance(idx=0)
# print(sample_network)

# sample_network = pipe.get_neg_instance(idx=0)
# print(sample_network)

# print(pipe.obs)

# print('positive benchmark: ',pipe.construct_pos_benchmark())
# print('negative benchmark: ',pipe.construct_neg_benchmark())

# pipe.show_results()

# path = 'test.txt'
# f = open(path,'w')
# labels = ["A","B","C"]
# res = [1,2,3]
# for label in labels:
#     f.write(label+',')
# f.write('\n')
# for r in res:
#     f.write(str(r)+',')
# f.close()


from normlap import Pipeline
pipe = Pipeline(elist1,elist2)
pipe.show_results()