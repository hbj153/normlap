from collections import defaultdict
import networkx as nx

class Formatter:
    
    @staticmethod
    def edgelist_to_neighborhood(br):
        relation = defaultdict(set)
        for nodeArr in br:
            relation[nodeArr[0]].add(nodeArr[1])
            relation[nodeArr[1]].add(nodeArr[0])
        return relation

    @staticmethod
    def neighborhood_to_edgelist(N):
        '''
        neighborhood_to_edgelist(N)

        Convert node pairs in neighborhood format to edgelist format.

        Parameters
        ----------
        N: Input network in neighborhood formation. For example, N = {"A": {"B", "C"},"B":{"A"},"C":{"A"}}

        Returns
        -------
        edgelist: Output network in edgelist format like [("A","B"),("B","C")]

        '''
        edgelist = []
        for nodeArr in N.keys():
            for neighbor in N[nodeArr]:
                if (nodeArr,neighbor) not in edgelist and (neighbor,nodeArr) not in edgelist:
                    edgelist.append(tuple(sorted((nodeArr,neighbor))))
        return sorted(edgelist)
    
    @staticmethod
    def neighborhood_to_adjacency(N):
        '''
        neighborhood_to_adjacency(N)

        Convert network in neighborhood format to adjacency matrix format.

        Parameters
        ----------
        N: Input network in neighborhood formation. For example, N = {"A": {"B", "C"},"B":{"A"},"C":{"A"}}

        Returns
        -------
        nodelist: sorted nodelist corresponds to the adjacency matrix.
        A: Output network in adjacency matrix function.
        '''
        nodelist = sorted(N.keys())
        edgelist = Formatter.neighborhood_to_edgelist(N)
        G = nx.from_edgelist(edgelist)
        A = nx.to_numpy_matrix(G,nodelist=nodelist)
        return nodelist,A

    @staticmethod
    def edgelist_to_adjacency(edgelist):
        '''
        edgelist_to_adjacency(edgelist)

        Convert network in edgelist format to adjacency matrix format.

        Parameters
        ----------
        N: Input network in edgelist formation.

        Returns
        -------
        nodelist: sorted nodelist corresponds to the adjacency matrix.
        A: Output network in adjacency matrix function.
        '''
        N = Formatter.edgelist_to_neighborhood(edgelist)
        nodelist = sorted(N.keys())
        G = nx.from_edgelist(edgelist)
        A = nx.to_numpy_matrix(G,nodelist=nodelist)
        return nodelist,A