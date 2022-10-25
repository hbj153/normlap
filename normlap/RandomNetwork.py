import numpy as np
from Formatter import Formatter
from Helper import Helper
from RandomSubnetwork import RandomSubnetwork


class RandomNetwork:
    @staticmethod
    def optimize_alpha(G1dict0, iters=100):
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
        G1dict = Helper.dict_remove_self(G1dict0)  # remove self-interactions
        # reference degree sequence generated from G1
        degrees = Helper.cal_node_degree(G1dict)
        nodelist = G1dict.keys()
        alphas_tem = {}.fromkeys(nodelist, 1)
        alphas = {}.fromkeys(nodelist, 1)
        alphas_tem_value = np.array(Helper.dict_values(alphas_tem, nodelist))
        for itering in range(iters):
            Sigma = np.array([np.sum(ai/((ai*alphas_tem_value)+1)) for ai in alphas_tem_value]
                             ) - np.array([ai/(ai**2+1) for ai in alphas_tem_value])
            degree_value = np.array(Helper.dict_values(degrees, nodelist))
            alphas_tem_value = Sigma/degree_value
        for i, node in enumerate(nodelist):
            alphas[node] = alphas_tem_value[i]
        return alphas

    @staticmethod
    def optimize_alpha_with_stop(G1dict0, max_iters=1000, stopping_criterion=-1):
        '''
        optimize_alpha_with_stop(G1dict0, max_iters=1000, stopping_criterion=-1)

        Optimize the alpha for nodes in G1dict with stopping criterion.

        Parameters
        ----------
        G1dict0: Reference network in neighborhood format that provides the node degree constriants. For example, G1dict = {"A": {"B", "C"},"B":{"A"},"C":{"A"}}
        max_iters: The maximum number of iterations for updating alphas.
        stopping_criterion: The stopping criterion for updating alphas. If the relative difference between the new alpha and the old alpha is smaller than the stopping_criterion, the updating process will stop.

        Returns
        -------
        alphas: A dictionary contains the optimized alphas for each node.
        alpha_history: A list contains the alpha history for the probe node.
        cur_iter: The number of iterations when stop updating alphas.
        '''
        G1dict = Helper.dict_remove_self(G1dict0)  # remove self-interactions
        # reference degree sequence generated from G1
        degrees = Helper.cal_node_degree(G1dict)
        nodelist = G1dict.keys()
        alphas_history = []
        alphas_tem = {}.fromkeys(nodelist, 1)
        alphas = {}.fromkeys(nodelist, 1)
        alphas_tem_value = np.array(Helper.dict_values(alphas_tem, nodelist))
        #initialize relative change
        rel_change = [999]*len(nodelist)
        for itering in range(max_iters):
            cur_iter = itering
            # if meet the stopping criterion, stop updating alphas
            if max(rel_change) < stopping_criterion:
                break
            # if not meet the stopping criterion, continue updating alphas
            alphas_tem_prev = alphas_tem_value
            Sigma = np.array([np.sum(ai/((ai*alphas_tem_value)+1)) for ai in alphas_tem_value]
                             ) - np.array([ai/(ai**2+1) for ai in alphas_tem_value])
            degree_value = np.array(Helper.dict_values(degrees, nodelist))
            alphas_tem_value = Sigma/degree_value
            alphas_history.append(alphas_tem_value)
            # calculate the relative change of alphas
            diff = alphas_tem_value - alphas_tem_prev
            rel_change = abs(diff/alphas_tem_prev)
        # update alphas
        for i, node in enumerate(nodelist):
            alphas[node] = alphas_tem_value[i]
        return alphas, alphas_history, cur_iter

    @staticmethod
    def cal_Pij(alphas, selfNodes):
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
        alphas_value = np.array([Helper.dict_values(alphas, nodelist)])
        Pij = 1/(1+np.dot(alphas_value.T, alphas_value))
        Pij = Pij - np.diag(np.diag(Pij))
        for selfNode in selfNodes:
            if selfNode in nodelist:
                index = nodelist.index(selfNode)
                Pij[index][index] = 1
        return Pij, nodelist

    @staticmethod
    def construct_random_network(Pij, nodelist, selfNodes):
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
        Rij = np.random.random(size=(N, N))
        Rij = np.triu(Rij)+np.triu(Rij, k=1).T
        Aij = Rij.copy()
        Aij[Pij < Rij] = 0
        Aij[Pij > Rij] = 1
        indices = np.where(np.triu(Aij) > 0)
        nodelist = np.array(nodelist)
        Gsample = Helper.sort_elist(
            np.array([nodelist[indices[0]], nodelist[indices[1]]]).T)
        selfinters = [(node, node) for node in selfNodes]
        Gsample = list(set(Gsample).union(selfinters))
        return Gsample

    @staticmethod
    def alphas_iteration(G1dict0: list, alphas_init: dict = None, iters: int = 100):
        """alphas_iteration iterate updating alphas for given iterations.

        Parameters
        ----------
        G0dict0 : _type_
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

        G1dict = Helper.dict_remove_self(G1dict0)  # remove self-interactions
        nodelist = list(G1dict.keys())

        # reference degree sequence generated from G1alphas_tem = {}.fromkeys(nodelist,1)
        degrees = Helper.cal_node_degree(G1dict)
        degree_value = np.array(Helper.dict_values(degrees, nodelist))

        # initialize alphas
        alphas = {}.fromkeys(
            nodelist, 1) if alphas_init == None else alphas_init
        alphas_tem_value = np.array(Helper.dict_values(alphas, nodelist))

        for _ in range(iters):
            Sigma = np.array([np.sum(ai / ((ai * alphas_tem_value) + 1))
                              for ai in alphas_tem_value]) - np.array([ai / (ai**2 + 1) for ai in alphas_tem_value])
            alphas_tem_value = Sigma / degree_value

        for i, node in enumerate(nodelist):
            alphas[node] = alphas_tem_value[i]

        return alphas

    @staticmethod
    def cal_neg(a1elist: list, a2elist: list, alphas: dict):
        """cal_neg calculate the negative benchmark for a given alphas.

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
        float,float
            neg1_mean, neg1_sigma
        """
        # only calculate the links in the comparing network(a2elist). Other links will never overlap with the comparing network.
        P1 = RandomSubnetwork.cal_probability(
            a2elist, a1elist, alphas)
        Pv1 = {link: P1[link]*(1-P1[link]) for link in P1}
        # one side
        neg1_mean = sum([P1.get(link, 0) for link in a2elist])
        neg1_sigma = np.sqrt(sum([Pv1.get(link, 0) for link in a2elist]))
        return neg1_mean, neg1_sigma

    @staticmethod
    def optimize_neg(a1elist, a2elist, iters_start=100, neg_change_limit=1, iter_spacing=100, max_iterations=2000):
        '''
        optimize_neg(a1elist,a2elist,iters_start=1000,neg_change_limit=1,iter_spacing=1000,max_iterations=20000)

        Optimize the neg by stopping iterating alphas at a given criterion.

        Parameters
        ----------
        a1elist: network1 represented in the edgelist format.
        a2elist: network2 represented in the edgelist format.
        iters_start: the minimum iteration of alphas, default = 100
        neg_change_limit: the stopping criterion based on the absolute change of neg between iter_spacing iterations.
        iter_spacing: check the neg change every iter_spacing.
        max_iterations: The maximum iterations.

        Returns
        -------
        cur_iter: the stopped iteration
        neg_mean: the neg mean
        neg_sigma: the neg sigma

        '''
        G1dict = Formatter.edgelist_to_neighborhood(a1elist)
        a0elist = list(set(a1elist).union(a2elist))

        G1dict = Helper.dict_remove_self(G1dict)  # remove self-interactions
        # reference degree sequence generated from G1
        degrees = Helper.cal_node_degree(G1dict)

        # fisrt generate alphas for iters_start iterations
        alphas_prev = RandomNetwork.alphas_iteration(
            G1dict, alphas_init=None, iters=iters_start)
        neg_mean_prev, neg_sigma_prev = RandomNetwork.cal_neg(
            a1elist, a2elist, alphas=alphas_prev)
        # check neg for every iter_spacing
        for i in range(iters_start+iter_spacing, max_iterations+iter_spacing, iter_spacing):
            alphas = RandomNetwork.alphas_iteration(
                G1dict, alphas_init=alphas_prev, iters=iters_start)
            # check the change in neg
            neg_mean, neg_sigma = RandomNetwork.cal_neg(
                a1elist, a2elist, alphas=alphas)
            # check the absolute change in pos
            if abs(neg_mean - neg_mean_prev) < neg_change_limit:
                cur_iter = i  # record the stopped iter
                break  # stop iteration
            else:
                alphas_prev = alphas
                neg_mean_prev = neg_mean

        return neg_mean, neg_sigma, cur_iter
