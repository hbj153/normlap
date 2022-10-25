from Formatter import Formatter
import copy
import numpy as np

class Helper:

    def covert2id(elist):
        """covert2id Convert the nodes in given list to node_ids, return the mapping.

        Parameters
        ----------
        elist1 : list(tuple)
            The edge list of network 1.
        elist2 : list(tuple)
            The edge list of network 2.

        Returns
        -------
        dict
            id2node, node2id mapping.
        """
        id2node = {}
        node2id = {}

        nodes = set([node for pair in elist for node in pair])

        for i, node in enumerate(nodes):
            id2node[i] = node
            node2id[node] = i
        
        return id2node, node2id

    def cal_node_degree(G):
        '''
        cal_node_degree(G)

        Calculate the node degree for a given network.

        Parameters
        ----------
        G: Network in neighborhood format like Gdict = {"A": {"B", "C"},"B":{"A"},"C":{"A"}} or edgelist format.

        Returns
        -------
        degrees: A dictionary with node degrees of each node. Example: {'A': 2, 'B': 1, 'C': 1}
        '''
        if type(G)==list:
            Gdict = Formatter.edgelist_to_neighborhood(G)
        else:
            Gdict = G
        degrees = {}
        for i in Gdict:
            degrees[i]=len(Gdict[i])
        return degrees

    def dict_remove_self(dic):
        """dict_remove_self remove the self-loops in the given neighborhood list

        Parameters
        ----------
        dic : dict
            The network represented in the neighborhood list format. e.g. {"A": ["B","C"]}

        Returns
        -------
        dict
            The network represented in the neighborhood list format without self-loop.
        """
        dic1 = copy.deepcopy(dic)
        todeletes = []
        for node in dic1:
            if node in dic1[node]:
                dic1[node].remove(node)
            # if node only have self-loop, delete the node
            if not dic1[node]: 
                todeletes.append(node)
        for todelete in todeletes:
            del dic1[todelete]
        return dic1

    def dict_values(dict1,keys):
        '''
        dict_values(dict1,keys)

        Return the values by the order of a given key list. If the key is not in the dictionary, 0 is assigned for the given key.
        
        Parameters
        ----------
        dict1: Dictionary.
        keys: a list of keys.
        
        Returns
        -------
        dict_value: The values of dictionart following the order of given keys.
        '''
        degrees = []
        for cur_key in keys:
            if cur_key in dict1.keys():
                degrees.append(dict1[cur_key])
            else:
                degrees.append(0)
        #return [dict1[cur_key] for cur_key in keys]
        return degrees

    def sort_elist(elist,strip=True,selfLink=False):
        '''
        strip: if True, the gene name will change from "YAL034W-A" to "YAL034WA"
        selfLink: if False, self-interactions will be removed from the edgelist.
        '''
        if len(elist)==0 or type(elist[0][0])!=str: return list(set(sorted([tuple(sorted(x)) for x in elist])))

        if strip==True:
            res = list(set(sorted([tuple(sorted([x[0].replace("-",""),x[1].replace("-","")])) for x in elist])))
            #res = list(set(sorted([tuple(sorted([x[0].split("-")[0],x[1].split("-")[0]])) for x in elist])))
        else:
            res = list(set(sorted([tuple(sorted(x)) for x in elist])))
            
        if selfLink==False:
            res = [pair for pair in res if pair[0]!=pair[1]]
        
        return res

    def count_overlap(elist1,elist2):
        """count_overlap Conut the number of overlap between two list.

        Parameters
        ----------
        elist1 : list(tuple)
            The edgelist of network 1.
        elist2 : list(tuple)
            The edgelist of network 2.

        Returns
        -------
        int
            Number of overlap between the two networks.
        """
        return len(set(elist1).intersection(elist2))

    def find_selfNodes(a1dict):
        '''
        Find nodes that have self-interations in a given dictionary.
        '''
        selfNodes = []
        for node in a1dict:
            if node in a1dict[node]:
                selfNodes.append(node)
        return selfNodes

    def cal_score(ms,bs,bes,cs,ces):
        """cal_score Calculate the normalized overlap score and its standard deviation.
                f = (m-b)/(c-b)
                m is constant

        Parameters
        ----------
        ms : float or list
            Observed overlap.
        bs : float or list
            Negative benchmark.
        bes : float or list
            Standard deviation of the negative benchmark.
        cs : float or list
            Positive benchmark.
        ces : float or list
            Standard deviation of the positive benchmark.

        Returns
        -------
        float, float or list,list
            scores,score_sigmas
        """
        '''

        '''
        scores = []
        score_sigmas = []
        
        # if pass integers
        if type(ms)==int:
            ms,bs,bes,cs,ces = [ms],[bs],[bes],[cs],[ces]

        # if pass arrays    
        for m,b,be,c,ce in zip(ms,bs,bes,cs,ces):
            if c-b != 0:
                score = (m-b)/(c-b)
                score_sigma = (1/(c-b)**2)*np.sqrt((m-c)**2*be**2+(b-c)**2*ce**2)
            else:
                score = None
                score_sigma = None
            scores.append(score)
            score_sigmas.append(score_sigma)
            
        return scores,score_sigmas