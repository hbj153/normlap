from Helper import Helper
from Formatter import Formatter
import random
import numpy as np


class RandomSubnetwork:

    def optimize_alpha(G0dict0, G1dict0, iters=1000, probeNode=0):
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
        G0dict = Helper.dict_remove_self(G0dict0)  # remove self-interactions
        G1dict = Helper.dict_remove_self(G1dict0)  # remove self-interactions
        # reference degree sequence generated from G1
        degrees = Helper.cal_node_degree(G1dict)
        # initialize alphas for all nodes to 1
        alphas = {}.fromkeys(G1dict.keys(), 1)
        alpha_probe = []
        for itering in range(iters):
            # save the new alphas, update alphas until the end of iteration.
            alphas_tem = {}.fromkeys(G1dict.keys(), 1)
            for i in G1dict:
                Sigma = 0
                # only the links exsit in G0 will be counted.
                for j in G0dict[i]:
                    if j in G1dict.keys():  # if node j also in G1
                        Sigma += 1/(alphas[j]+1/alphas[i])
                alphas_tem[i] = Sigma/degrees[i]
            alphas.update(alphas_tem)
            if probeNode != None:
                alpha_probe.append(
                    [itering, alphas[list(G1dict.keys())[probeNode]]])
            #if itering+10>iters: print(alphas)
        return alphas, alpha_probe

    def optimize_alpha_with_stop(G0dict0, G1dict0, max_iters=1000, stopping_criterion=-1):
        '''
        optimize_alpha_with_stop(G0dict0,G1dict0,max_iters=1000,stopping_criterion = -1):

        Optimize the alpha for nodes in G1dict.

        Parameters
        ----------
        G0dict: Complete network in neighborhood format. For example, N = {"A": {"B", "C"},"B":{"A"},"C":{"A"}}
        G1dict: Reference network in neighborhood format that provides the node degree constriants.
        max_iters: The maximum number of iterations for updating alphas.
        stopping_criterion: The stopping criterion for updating alphas. If the relative difference between the new alpha and the old alpha is smaller than the stopping_criterion, the updating process will stop.

        Returns
        -------
        alphas: A dictionary contains the optimized alphas for each node.
        alpha_history: A list contains the alpha history for the probe node.
        cur_iter: The number of iterations when stop updating alphas.
        '''

        G0dict = Helper.dict_remove_self(G0dict0)  # remove self-interactions
        G1dict = Helper.dict_remove_self(G1dict0)  # remove self-interactions
        # reference degree sequence generated from G1
        degrees = Helper.cal_node_degree(G1dict)
        # initialize alphas for all nodes to 1
        alphas = {}.fromkeys(G1dict.keys(), 1)
        alphas_history = []
        rel_change = {}.fromkeys(G1dict.keys(), 999)
        alpha_probe = []
        for itering in range(max_iters):
            cur_iter = itering
            # if the maximum relative change of alphas is smaller than the stopping criterion, stop updating alphas.
            if max(rel_change.values()) < stopping_criterion:
                break
            # save the new alphas to alphas_tem, update alphas until the end of iteration.
            alphas_tem = {}.fromkeys(G1dict.keys(), 1)
            for i in G1dict:
                Sigma = 0
                # only the links exsit in G0 will be counted.
                for j in G0dict[i]:
                    # if node j also in G1, otherwise degrees[j]=0
                    if j in G1dict.keys():
                        Sigma += 1 / (alphas[j] + 1 / alphas[i])
                alphas_tem[i] = Sigma / degrees[i]
                diff = (alphas_tem[i] - alphas[i])
                rel_change[i] = abs(diff / alphas[i])
            alphas.update(alphas_tem)
            alphas_history.append(list(alphas.values()))

        return alphas, alphas_history, cur_iter

    def cal_probability(G0elist, G1elist, alphas):
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
            if link[0] == link[1]:  # self-interactions
                if link in G1elist:  # exsit in G1
                    probs[link] = 1
                else:  # self-interaction not exsit in G1
                    probs[link] = 0
            else:  # not self-interactions
                # Only count links that both nodes in alpha dict
                if link[0] in alphas.keys() and link[1] in alphas.keys():
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
            if prob >= rand:
                Gsample.append(i)
        return Gsample

    @staticmethod
    def alphas_iteration(G0dict, G1dict, degrees, alphas_init: dict = None, iters: int = 1000):
        """alphas_iteration iterate updating alphas for given iterations.

        Parameters
        ----------
        G0dict : _type_
            _description_
        G1dict : _type_
            _description_
        degrees : _type_
            _description_
        alphas_init : dict, optional
            _description_, by default None
        iters : int, optional
            _description_, by default 1000

        Returns
        -------
        _type_
            _description_
        """
        # initialize alphas
        alphas = {}.fromkeys(
            G1dict.keys(), 1) if alphas_init == None else alphas_init
        for itering in range(iters):
            # save the new alphas, update alphas until the end of iteration.
            alphas_tem = {}.fromkeys(G1dict.keys(), 1)
            for i in G1dict:
                Sigma = 0
                # only the links exsit in G0 will be counted.
                for j in G0dict[i]:
                    # if node j also in G1, otherwise degrees[j]=0
                    if j in G1dict.keys():
                        Sigma += 1 / (alphas[j] + 1 / alphas[i])
                alphas_tem[i] = Sigma / degrees[i]
            alphas.update(alphas_tem)
        return alphas

    @staticmethod
    def cal_pos(a1elist: list, a2elist: list, alphas: dict):
        """cal_pos calculate the positive benchmark for a given alphas.

        Parameters
        ----------
        a1elist : list
            _description_
        a2elist : list
            _description_
        alphas : dict
            _description_

        Returns
        -------
        _type_
            _description_
        """
        # alphas of a1elist
        # only calculate the probability if links also in a2elist, otherwise, it won't overlap with a1elist
        P1 = RandomSubnetwork.cal_probability(a2elist, a1elist, alphas=alphas)
        Pv1 = {link: P1[link]*(1-P1[link]) for link in P1}
        pos1_mean = sum([P1.get(link, 0) for link in a2elist])
        pos1_sigma = np.sqrt(sum([Pv1.get(link, 0) for link in a2elist]))
        return pos1_mean, pos1_sigma

    @staticmethod
    def optimize_pos(a1elist, a2elist, iters_start=1000, pos_change_limit=1, iter_spacing=1000, max_iterations=20000):
        '''
        optimize_pos(a1elist,a2elist,iters_start=1000,pos_change_limit=1,iter_spacing=1000,max_iterations=20000)

        Optimize the pos by stopping iterating alphas at a given criterion.

        Parameters
        ----------
        a1elist: network1 represented in the edgelist format.
        a2elist: network2 represented in the edgelist format.  
        iters_start: the minimum iteration of alphas, default = 1000
        pos_change_limit: the stopping criterion based on the absolute change of pos between iter_spacing iterations.
        iter_spacing: check the pos change every iter_spacing.
        max_iterations: The maximum iterations.

        Returns
        -------
        cur_iter: the stopped iteration
        pos_mean: the pos mean
        pos_sigma: the pos sigma

        '''
        G1dict = Formatter.edgelist_to_neighborhood(a1elist)
        a0elist = list(set(a1elist).union(a2elist))
        G0dict = Formatter.edgelist_to_neighborhood(a0elist)

        G0dict = Helper.dict_remove_self(G0dict)  # remove self-interactions
        G1dict = Helper.dict_remove_self(G1dict)  # remove self-interactions
        # reference degree sequence generated from G1
        degrees = Helper.cal_node_degree(G1dict)
        # fisrt generate alphas for iters_start iterations
        alphas_prev = RandomSubnetwork.alphas_iteration(
            G0dict, G1dict, degrees, alphas_init=None, iters=iters_start)
        pos_mean_prev, pos_sigma_prev = RandomSubnetwork.cal_pos(
            a1elist, a2elist, alphas=alphas_prev)
        # check pos for every iter_spacing
        for i in range(iters_start+iter_spacing, max_iterations+iter_spacing, iter_spacing):
            alphas = RandomSubnetwork.alphas_iteration(
                G0dict, G1dict, degrees, alphas_init=alphas_prev, iters=iters_start)
            # check the change in pos
            pos_mean, pos_sigma = RandomSubnetwork.cal_pos(
                a1elist, a2elist, alphas=alphas)
            # check the absolute change in pos
            if abs(pos_mean - pos_mean_prev) < pos_change_limit:
                cur_iter = i  # record the stopped iter
                break  # stop iteration
            else:
                alphas_prev = alphas
                pos_mean_prev = pos_mean

        return pos_mean, pos_sigma, cur_iter
