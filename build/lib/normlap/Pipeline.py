
from Helper import Helper
from Formatter import Formatter
from RandomNetwork import RandomNetwork
from RandomSubnetwork import RandomSubnetwork
import numpy as np
import scipy

# @TODO: add function to generate random network based on the optimized alpha

class Pipeline:
    """ Pipeline for comparing overlap between two networks.
    This pipeline uses the default criterion for updating alphas as follows:
    1. The alphas for positive benchmark stop updating when the difference between the current and previous pos mean is less than 1.
    2. The alphas for negative benchmark stop updating when the difference between the current and previous neg mean is less than 1.
    """
    
    def __init__(self,elist1:list, elist2:list, poollist: list=None) -> None:
        """__init__ initialize the pipeline

        Parameters
        ----------
        elist1 : list
            network1 in edge list format.
        elist2 : list
            network2 in edge list format.
        poollist : list, optional
            The pool of generating the instance, by default None, meaning the pool is the union of the two network.
        """
        # if the pool is not given
        if poollist == None:
            self.poollist = list(set(elist1).union(elist2))
        else:
            self.poollist = poollist

        self.pos_iter = 1000
        self.neg_iter = 1000

        # convert node to node_ids
        self.id2node, self.node2id = Helper.covert2id(self.poollist)
        self.elist1 = [(self.node2id[node1],self.node2id[node2]) for node1,node2 in elist1]
        self.elist2 = [(self.node2id[node1],self.node2id[node2]) for node1,node2 in elist2]
        self.poollist = [(self.node2id[node1],self.node2id[node2]) for node1,node2 in self.poollist]

        # convert to neighborhood
        self.a1dict = Formatter.edgelist_to_neighborhood(self.elist1)
        self.a2dict = Formatter.edgelist_to_neighborhood(self.elist2)

        # observed overlap
        self.obs = Helper.count_overlap(self.elist1, self.elist2)

        self.pos_mean = None
        self.neg_mean = None
    
    def get_pos_instance(self, idx: int=0):
        """get_pos_instance Generate an instance of positive benchmark.

        Parameters
        ----------
        aelist : list, optional
            The pool of generating the instance, by default None, meaning the pool is the union of the two network.
        idx : int, optional
            The index of the reference network, by default 0, meaning the instance has the same degree sequence with network1; 
            else, the instance has the same degree sequecne with network2.

        Returns
        -------
        list(tuple)
            An instance of the positive benchmark in egde list format.
        """
        
        ## positive benchmark
        aelist = self.poollist
        adict = Formatter.edgelist_to_neighborhood(aelist)
        if idx==0:
            alphas,_ = RandomSubnetwork.optimize_alpha(adict,self.a1dict,iters=self.pos_iter,probeNode=0)
            P = RandomSubnetwork.cal_probability(aelist,self.elist1,alphas=alphas)
        else:
            alphas,_ = RandomSubnetwork.optimize_alpha(adict,self.a2dict,iters=self.pos_iter,probeNode=0)
            P = RandomSubnetwork.cal_probability(aelist,self.elist2,alphas=alphas)
        Gpos = RandomSubnetwork.construct_sample_network(P)
        Gpos = [(self.id2node[node1],self.id2node[node2])for node1,node2 in Gpos]
        return Gpos

    def get_neg_instance(self, idx: int=0):
        """get_neg_instance Generate an instance of negative benchmark.

        Parameters
        ----------
        idx : int, optional
            The index of the reference network, by default 0, meaning the instance has the same degree sequence with network1; 
            else, the instance has the same degree sequecne with network2.

        Returns
        -------
        list(tuple)
            An instance of the negative benchmark in egde list format.
        """

        ## negative benchmark
        if idx==0:
            alphas_zero = RandomNetwork.optimize_alpha(self.a1dict,iters=self.neg_iter)
            selfNodes = Helper.find_selfNodes(self.a1dict)
            Pij,nodelist = RandomNetwork.cal_Pij(alphas_zero,selfNodes)
        else:
            alphas_zero = RandomNetwork.optimize_alpha(self.a2dict,iters=self.neg_iter)
            selfNodes = Helper.find_selfNodes(self.a2dict)
            Pij,nodelist = RandomNetwork.cal_Pij(alphas_zero,selfNodes)
        Gneg = RandomNetwork.construct_random_network(Pij,nodelist,selfNodes)
        Gneg = [(self.id2node[node1],self.id2node[node2])for node1,node2 in Gneg]
        return Gneg

    def get_pos_benchmark(self, iters_start:int=1000, pos_change_limit=1, iter_spacing:int=1000, max_iterations:int=20000):
        """get_pos_benchmark Generate the positive benchmark.

        Parameters
        ----------
        iters_start : int, optional
            The number of iterations to start with, by default 1000.
        pos_change_limit : int, optional
            The change limit for updating the number of iterations, by default 1.
        iter_spacing : int, optional
            The spacing between two iterations, by default 1000.
        max_iterations : int, optional
            The maximum number of iterations, by default 20000.

        Returns
        -------
        pos_mean : float
            The mean of the positive benchmark.
        pos_sigma : float
            The standard deviation of the positive benchmark.
        """
        self.pos1_mean, self.pos1_sigma, self.cur_iter_pos1 = RandomSubnetwork.optimize_pos(
            self.elist1, self.elist2, iters_start=iters_start, pos_change_limit=pos_change_limit, iter_spacing=iter_spacing, max_iterations=max_iterations)
        self.pos2_mean, self.pos2_sigma, self.cur_iter_pos2 = RandomSubnetwork.optimize_pos(
            self.elist2, self.elist1, iters_start=iters_start, pos_change_limit=pos_change_limit, iter_spacing=iter_spacing, max_iterations=max_iterations)

        # select the positive benchmark that is closer to the observed overlap
        z1 = abs((self.obs - self.pos1_mean) / self.pos1_sigma)
        z2 = abs((self.obs - self.pos2_mean) / self.pos2_sigma)

        if z1 < z2:
            self.pos_mean, self.pos_sigma = self.pos1_mean, self.pos1_sigma
        else:
            self.pos_mean, self.pos_sigma = self.pos2_mean, self.pos2_sigma

        return self.pos_mean, self.pos_sigma

    def get_neg_benchmark(self, iters_start:int=100, neg_change_limit=1, iter_spacing:int=1000, max_iterations:int=5000):
        """get_neg_benchmark Generate the negative benchmark.

        Parameters
        ----------
        iters_start : int, optional
            The number of iterations to start with, by default 100.
        neg_change_limit : int, optional
            The change limit for updating the number of iterations, by default 1.
        iter_spacing : int, optional
            The spacing between two iterations, by default 1000.
        max_iterations : int, optional
            The maximum number of iterations, by default 5000.

        Returns
        -------
        neg_mean : float
            The mean of the negative benchmark.
        neg_sigma : float
            The standard deviation of the negative benchmark.
        """
        self.neg1_mean, self.neg1_sigma, self.cur_iter_neg1 = RandomNetwork.optimize_neg(
            self.elist1, self.elist2, iters_start=iters_start, neg_change_limit=neg_change_limit, iter_spacing=iter_spacing, max_iterations=max_iterations)
        self.neg2_mean, self.neg2_sigma, self.cur_iter_neg2 = RandomNetwork.optimize_neg(
            self.elist2, self.elist1, iters_start=iters_start, neg_change_limit=neg_change_limit, iter_spacing=iter_spacing, max_iterations=max_iterations)

        # select the negative benchmark that is closer to the observed overlap
        z1 = abs((self.obs - self.neg1_mean) / self.neg1_sigma)
        z2 = abs((self.obs - self.neg2_mean) / self.neg2_sigma)

        if z1 < z2:
            self.neg_mean, self.neg_sigma = self.neg1_mean, self.neg1_sigma
        else:
            self.neg_mean, self.neg_sigma = self.neg2_mean, self.neg2_sigma

        return self.neg_mean, self.neg_sigma

    def construct_pos_benchmark(self):
        """
        Note that this function is deprecated. Please use get_pos_benchmark instead.
        construct_pos_benchmark Construct the positive benchmark for the given two networks.

        Parameters
        ----------
        aelist : list, optional
            The pool of generating the instance, by default None, meaning the pool is the union of the two network.

        Returns
        -------
        float,float
            pos_mean,pos_sigma
        """
        aelist = self.poollist
        adict = Formatter.edgelist_to_neighborhood(aelist)

        alphas1,_ = RandomSubnetwork.optimize_alpha(adict,self.a1dict,iters=self.pos_iter,probeNode=0)
        alphas2,_ = RandomSubnetwork.optimize_alpha(adict,self.a2dict,iters=self.pos_iter,probeNode=0)
        # average probability
        P1 = RandomSubnetwork.cal_probability(aelist,self.elist1,alphas=alphas1)
        P2 = RandomSubnetwork.cal_probability(aelist,self.elist2,alphas=alphas2)
        # variance probability
        Pv1 = {link: P1[link]*(1-P1[link]) for link in P1 }
        Pv2 = {link: P2[link]*(1-P2[link]) for link in P2 }
        # benchmarks
            # one side
        self.pos1_mean = sum([P1.get(link,0) for link in self.elist2])
        self.pos1_sigma = np.sqrt(sum([Pv1.get(link,0) for link in self.elist2])) + 0.00001 # avoid zero
        self.pos2_mean = sum([P2.get(link,0) for link in self.elist1])
        self.pos2_sigma = np.sqrt(sum([Pv2.get(link,0) for link in self.elist1])) + 0.00001 # avoid zero
        z1 = abs((self.obs - self.pos1_mean) / self.pos1_sigma)
        z2 = abs((self.obs - self.pos2_mean) / self.pos2_sigma)

        if z1<z2:
            self.pos_mean, self.pos_sigma =  self.pos1_mean,self.pos1_sigma
        else:
            self.pos_mean, self.pos_sigma =  self.pos2_mean,self.pos2_sigma
        
        return self.pos_mean, self.pos_sigma

    def construct_neg_benchmark(self):
        """
        Note that this function is deprecated. Please use get_neg_benchmark instead.
        """

        # neg1
        alphas1_neg = RandomNetwork.optimize_alpha(self.a1dict,iters=self.neg_iter)
        # only calculate the links in the comparing network(a2elist). Other links will never overlap with the comparing network.
        P1 = RandomSubnetwork.cal_probability(self.elist2,self.elist1,alphas1_neg) 
        Pv1 = {link: P1[link]*(1-P1[link]) for link in P1 }
        # one side
        self.neg1_mean = sum([P1.get(link,0) for link in self.elist2])
        self.neg1_sigma = np.sqrt(sum([Pv1.get(link,0) for link in self.elist2])) + 0.00001 # avoid zero

        # neg2
        alphas2_neg = RandomNetwork.optimize_alpha(self.a2dict,iters=self.neg_iter)
        # only calculate the links in the comparing network(a1elist). Other links will never overlap with the comparing network.
        P2 = RandomSubnetwork.cal_probability(self.elist1,self.elist2,alphas2_neg) 
        Pv2 = {link: P2[link]*(1-P2[link]) for link in P2 }
        # one side
        self.neg2_mean = sum([P2.get(link,0) for link in self.elist1])
        self.neg2_sigma = np.sqrt(sum([Pv2.get(link,0) for link in self.elist1])) + 0.00001 # avoid zero

        z1 = abs((self.obs - self.neg1_mean) / self.neg1_sigma)
        z2 = abs((self.obs - self.neg2_mean) / self.neg2_sigma)

        if z1<z2:
            self.neg_mean, self.neg_sigma =  self.neg1_mean,self.neg1_sigma
        else:
            self.neg_mean, self.neg_sigma =  self.neg2_mean,self.neg2_sigma
        
        return self.neg_mean, self.neg_sigma

    def plot(self):
        pass

    def show_results(self, printOn: bool=True):
        if not self.pos_mean:
            print("The get_pos_benchmark function has not been called yet. The results will be calculated based on default parameters.")
            self.pos_mean, self.pos_sigma = self.get_pos_benchmark()
        if not self.neg_mean:
            print("The get_neg_benchmark function has not been called yet. The results will be calculated based on default parameters.")
            self.neg_mean, self.neg_sigma = self.get_neg_benchmark()

        self.neg_z = (self.obs-self.neg_mean)/self.neg_sigma if self.neg_sigma!=0 else np.nan
        self.neg_p = scipy.stats.norm.sf(self.neg_z)
        self.pos_z = (self.obs-self.pos_mean)/self.pos_sigma if self.pos_sigma!=0 else np.nan
        self.pos_p = 1 - scipy.stats.norm.sf(self.pos_z)
        self.normlap, self.normlap_sigma = Helper.cal_score(self.obs,self.neg_mean,self.neg_sigma,self.pos_mean,self.pos_sigma)
        self.normlap, self.normlap_sigma = self.normlap[0], self.normlap_sigma[0]

        labels = ["Observed overlap","Neg_mean","Neg_sigma","Neg_p","Pos_mean","Pos_sigma","Pos_p","Normlap","Normlap_sigma"]
        res = [self.obs, self.neg_mean, self.neg_sigma, self.neg_p, self.pos_mean, self.pos_sigma, self.pos_p,self.normlap,self.normlap_sigma]
        if printOn:
            for label, num in zip(labels,res):
                if num != np.nan or None:
                    print(label+': ', '%.2f'%num)
                else:
                    print(label+': None')

        return labels, res
        


    