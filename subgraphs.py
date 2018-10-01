import collections
import networkx as nx
import numpy as np

class subGraph(nx.Graph):
    """A few additions to networkx's graph class to compute and store subgraph 
    statistics.
    """

    def calcCornerCounts(self, D):
        """Return the number of corners, where the number of edges that connect
        a node to a subgraph define a corner.
        """
        count = collections.defaultdict(lambda: 0)
        for d in D: 
            count[int(d)] += 1
        return count 

    def add_edges_from(self, ebunch_to_add, **attr):
        super().add_edges_from(ebunch_to_add, **attr)
        self.computeStatistics()

    def computeStatistics(self):

        self._D = [n[1] for n in list(self.degree)]
        self._m = sum(self._D)
        self._cornerTypes = list(set(self._D))
        self._totalCorners = len(self._cornerTypes)
        self._cornerCounts = self.calcCornerCounts(self._D)
        C = list(self._cornerCounts.values())
        
        #TODO: corner positions in larger asymmetric subgraphs can not be 
        #      specified. 
        self._cornerDist = [c/sum(C) for c in C]

    @property
    def D(self):
        return self._D

    @property
    def m(self):
        return self._m

    @property
    def cornerTypes(self):
        return self._cornerTypes

    @property
    def cornerCounts(self):
        return self._cornerCounts
    
    @property
    def cornerDist(self):
        return self._cornerDist

    @property
    def totalCorners(self):
        return self._totalCorners
    
    
class subGraphSequence:
    """A class to manage to manipulation of subgraph sequences. 
    """

    def __init__(self, S, s): 
        """    
        Parameters
        ----------
        S : array_like
            The subgraph sequence. A sequence of ints of subgraph degrees. This 
            sequence specifies only how many times a node touches a subgraph, 
            i.e., is irrespective of a node's position within the subgraph. 
        s : object 
            A subgraph object. 
        """
        self._subgraphSequence = np.random.shuffle(S) 
        self._subgraph = s 
        self._resolvedPositions = self._resolvePositions(S, s.cornerDist)
        self._requiredStubs = np.array([np.dot(n, s.cornerTypes) for n in self._resolvedPositions])
        # Left of this index has been allocated to nodes. 
        self.index = 0
        # A sequence of tuples whos order corresponds to the degree sequence. 
        self._allocated_sequence = np.zeros( shape=(s.totalCorners, len(S)) )

    @property
    def subgraphSequence(self):
        return self._subgraphSequence

    @property
    def subgraph(self):
        return self._subgraph

    @property
    def resolvedPositions(self):
        return self._resolvedPositions
    
    @property
    def requiredStubs(self):
        return self._requiredStubs

    @property
    def allocated_sequence(self):
        return self._allocated_sequence
    
    
    def _resolvePositions(self, S, cornerDist):
        """For asymmetric subgraphs a node's position matters. This method 
        multinomially resolves this ambiguity.
        
        Parameters
        ---------- 
        S : array_like
            The subgraph sequence. 
        cornerDist : array_like
            An array of probabilities specifying the distribution of corners in 
            the given subgraph.
        Returns
        -------
        Sp : array_like. 
             A subgraph sequence with positions specified. For a subgraph with l
             different positions in a network of N individuals this array will 
             have [N x l] dimensions. 
        """
        return np.array([np.random.multinomial(n, cornerDist) for n in S])

    def get_corner(self): 
        corner = np.multiply(s.cornerTypes, self._resolvePositions[self.index])
        self.index+=1
        return corner 




# a.flags.writeable = False
