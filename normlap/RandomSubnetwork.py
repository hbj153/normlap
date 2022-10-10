
from .Helper import Helper
import random

class RandomSubnetwork:

    def optimize_alpha(G0dict0,G1dict0,iters=1000,probeNode=0):
        
        '''
        optimize_alpha(G0dict,G1dict,iters=1000,probeNode=0

        Optimize the alpha for nodes in G1dict.

        Parameters
        ----------
        G0dict: Complete network in neighborhood format. For example, N = {"A": {"B", "C"},"B":{"A"},"C":{"A"}}
        G1dict: Reference network in neighborhood format that provides the node degree constriants.
        iters: The number of iterations for updating alphas.
        probeNode: The index of the probe node. The alpha history will be returned for the probe node.

        Returns
        -------
        alphas: A dictionary contains the optimized alphas for each node.
        alpha_probe: A list contains the history alphas for the probleNode.
        '''
        G0dict = Helper.dict_remove_self(G0dict0) # remove self-interactions
        G1dict = Helper.dict_remove_self(G1dict0) # remove self-interactions
        degrees = Helper.cal_node_degree(G1dict) # reference degree sequence generated from G1
        alphas = {}.fromkeys(G1dict.keys(),1) # initialize alphas for all nodes to 1
        alpha_probe = []
        for itering in range(iters):
            alphas_tem = {}.fromkeys(G1dict.keys(),1) # save the new alphas, update alphas until the end of iteration.
            for i in G1dict:
                Sigma = 0
                for j in G0dict[i]: # only the links exsit in G0 will be counted.
                    if j in G1dict.keys(): # if node j also in G1
                        Sigma += 1/(alphas[j]+1/alphas[i])
                alphas_tem[i] = Sigma/degrees[i]
            alphas.update(alphas_tem)
            if probeNode != None:
                alpha_probe.append([itering,alphas[list(G1dict.keys())[probeNode]]])
            #if itering+10>iters: print(alphas)
        return alphas,alpha_probe
    
    def cal_probability(G0elist,G1elist,alphas):

        '''
        cal_probability(G0elist,alphas)

        Calculate the probability for links in G0elist.

        Parameters
        ----------
        G0elist: The complete network in edgelist format. Example: G0elist = [('A', 'B'), ('A', 'C')]
        G1elist: Reference network in neighborhood format that provides the node degree constriants. Here it is used to determine whether a self-interaction si allowed.
                If (i,i) in G1elist, pii=1, else, pii=0.
        alphas: The optimized alphas for each node(of G1, the reference network).

        Returns
        -------
        probs: A dictionary contains the connection probability of the edges in G0elist.
        '''

        probs = {}
        for link in G0elist:
            if link[0]==link[1]: # self-interactions 
                if link in G1elist: # exsit in G1
                    probs[link] = 1
                else: # self-interaction not exsit in G1
                    probs[link] = 0
            else: # not self-interactions
                if link[0] in alphas.keys() and link[1] in alphas.keys(): # Only count links that both nodes in alpha dict
                    probs[link] = 1/(1+alphas[link[0]]*alphas[link[1]])
        return probs
    
    def construct_sample_network(probs):
        '''
        construct_sample_network(probs)

        Construct sample network according to the connection probability provided by probs.

        Parameters
        ----------
        probs: A dictionary contains the connection probability of the links(of G0, the complete network). Example: {(1, 3): 0.99, (1, 4): 0.96}.

        Returns
        -------
        Gsample: Constructed sample network according to probs in edgelist format.
        '''
        Gsample = []
        for i in probs:
            prob = probs[i]
            rand = random.random()
            if prob>=rand:
                Gsample.append(i)
        return Gsample
