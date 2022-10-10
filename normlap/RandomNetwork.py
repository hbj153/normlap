from .Helper import Helper
import numpy as np


class RandomNetwork:
    @staticmethod
    def optimize_alpha(G1dict0,iters=100): # 更快,可以用！
        
        '''
        optimize_alpha(G1dict0,iters=100)

        Optimize the alpha for nodes in G1dict.

        Parameters
        ----------
        G1dict0: Reference network in neighborhood format that provides the node degree constriants.
        iters: The number of iterations for updating alphas.

        Returns
        -------
        alphas: A dictionary contains the optimized alphas for each node.
        '''
        G1dict = Helper.dict_remove_self(G1dict0) # remove self-interactions
        degrees = Helper.cal_node_degree(G1dict) # reference degree sequence generated from G1
        nodelist = G1dict.keys()
        alphas_tem = {}.fromkeys(nodelist,1)
        alphas = {}.fromkeys(nodelist,1)
        alphas_tem_value = np.array(Helper.dict_values(alphas_tem,nodelist))
        for itering in range(iters):
            Sigma = np.array([np.sum(ai/((ai*alphas_tem_value)+1)) for ai in alphas_tem_value]) - np.array([ai/(ai**2+1) for ai in alphas_tem_value])
            degree_value = np.array(Helper.dict_values(degrees,nodelist))
            alphas_tem_value = Sigma/degree_value
        for i,node in enumerate(nodelist):
            alphas[node] = alphas_tem_value[i]
        return alphas
    
    @staticmethod
    def cal_Pij(alphas,selfNodes):
        '''
        cal_Pij(alphas,selfNodes)

        Calculate the probability matrix for all possible combinations of nodes in alphas. Self-interactions Pii=1.

        Parameters
        ----------
        alphas: The optimized alphas for each node(of G1, the reference network).
        selfNodes: The nodes that have self-interactions in G1(the reference network).

        Returns
        -------
        Pij: The probability matrix following the order given by nodelist.
        nodelist: Provide the reference of the order of the probability matrix Pij.

        '''
        nodelist = sorted(alphas.keys())
        alphas_value = np.array([Helper.dict_values(alphas,nodelist)])
        Pij = 1/(1+np.dot(alphas_value.T,alphas_value))
        Pij = Pij - np.diag(np.diag(Pij))
        for selfNode in selfNodes:
            if selfNode in nodelist:
                index = nodelist.index(selfNode)
                Pij[index][index] = 1
        return Pij,nodelist

    @staticmethod
    def construct_random_network(Pij,nodelist,selfNodes):
        '''
        construct_random_network(Pij,nodelist), self-interactions are preserved.

        Construct the random network according to the given probability matrix Pij.

        Parameters
        ----------
        Pij: The probability matrix following the order given by nodelist.
        nodelist: Provide the reference of the order of the probability matrix Pij.
        selfNodes: The nodes that have self-interactions in G1(the reference network).

        Returns
        -------
        Gsample: random network in edgelist format.

        '''
        N = len(Pij)
        Rij = np.random.random(size=(N,N))
        Rij = np.triu(Rij)+np.triu(Rij,k=1).T
        Aij = Rij.copy()
        Aij[Pij<Rij]=0
        Aij[Pij>Rij]=1
        indices = np.where(np.triu(Aij)>0)
        nodelist = np.array(nodelist)
        Gsample = Helper.sort_elist(np.array([nodelist[indices[0]],nodelist[indices[1]]]).T)
        selfinters = [(node,node) for node in selfNodes]
        Gsample = list(set(Gsample).union(selfinters))
        return Gsample 
    