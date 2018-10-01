import networkx as nx 
import numpy as np 
import sys

class HyperStubAllocation:
    """This class allocates corners of subgraphs to nodes, i.e., it orders the
    subgraph sequences. 
    """

    def __init__(self, degree_sequence, sequences_list, subgraph_list):
        """    
        Parameters
        ----------
        degree_sequence : array_like
                        : The target degree sequence of the network. 
        sequences_list  : list of sequence objects
                        : The target sequence for a subgraph, contained within
                        : a subGraphSequence object. 
        subgraph_list   : list of subgraph objects
                        : A networkx realisation of the subgraph, contained 
                        : within a subGraph object. This list needs to share the
                        : same ordering as sequences_list.                         
        Variables
        ---------
        _total_corners : int
        hyper_stub_sequences : array_like 

        """

        self.check_D_is_even(degree_sequence)
        self._N = len(degree_sequence)

        # Within this class the order of the degree sequence is sacrosanct.  
        self._D = degree_sequence
        self._bins, self._freq = self.compute_node_counts(degree_sequence)

        # The values of the subgraph sequences are sacrosanct, but there order 
        # is not. A particular value within a subgraph sequence needs to be 
        # to a node with a sufficient number of edges to construct that corner 
        # type. 
        self._subgraph_sequences = sequences_list
        self._subgraphs          = subgraph_list
        
        self._total_corners = [subg.totalCorners for subg in subgraph_list]
        self._total_corners = np.sum(self._total_corners)
        
        # self.hyper_stub_sequences = np.zeros(self._total_corners+1, self._N) 
        # self.hyper_stub_sequences[0,:] = degree_sequence 
        self.remaining_stubs  = degree_sequence
        self.cum_remain_count = self._D_cumulative_counts(self.remaining_stubs) 

    def check_D_is_even(self, degree_sequence):
        if sum(degree_sequence) % 2 != 0: 
            raise ValueError('The degree sequence must sum to an even number.')
            sys.exit()


    def compute_node_counts(self, D):
        """The cumulative count of degree is used when selecting nodes to 
        accommodate subgraph corners. 
        Parameters
        ----------
        D : array_like
          : The target degree sequence of the network.    
        """
        idx = np.arange(len(D))
        bins = {i: [] for i in range(D.max()+1)}
        for i, d in enumerate(D):
            bins[d].append(i)
            freq = np.array([len(i) for i in bins.values()])

        return bins, freq 

    def _select_accomidating_node(self, min_degree):
        """Selects a node with degree >= min_degree proportional to how many 
        nodes there are of a given degree.  
        """
        if self.remaining_stubs.max() < min_degree:
            raise ValueError(( 'The lower bound on desired stubs exceeds the '
                               'maximum available degree.') )
            sys.exit()
        else:
            freq = self.freq[min_degree:]
            choice = np.random.choice( np.arange(min_degree, self._D.max()+1), 
                                       p=freq/sum(freq))
            node = self.bins[choice].pop()
            self.freq[min_degree + choice ] -= 1 
            return node 

    def _allocate_subgraphs_to_nodes():
        """
        """

        # Condition: every subgraph corner in a given sequence has been 
        # considered. 
        lambda condition x: x.index<self._N 
        while any(map(condition, self._subgraph_sequences)):
            corner, subgraph_index = self._select_corner()
            node = self._select_accomidating_node( sum(corner) )
            self.remaining_stubs[node] -= sum(corner)
            self._subgraph_sequences.allocated_sequence[node] = corner 




    def _select_corner(): 
        """Select a corner at random.
        """
        choice = np.random.choice(len(self._subgraph_sequences))
        return self._subgraph_sequences[choice].get_corner(), choice 

