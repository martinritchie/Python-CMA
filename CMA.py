import networkx as nx 
import numpy as np 
import random
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
        self._bins, self._freq = self.cumulative_degree_counts(degree_sequence)

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
        self.bins, self.freq = self.cumulative_degree_counts(
                                   self.remaining_stubs)

    def check_D_is_even(self, degree_sequence):
        if sum(degree_sequence) % 2 != 0: 
            raise ValueError('The degree sequence must sum to an even number.')
            sys.exit()

    def cumulative_degree_counts(self, D):
        """The cumulative count of degree is used when selecting nodes to 
        accommodate subgraph corners. 
        Parameters
        ----------
        D : array_like
          : The target degree sequence of the network.
        Returns
        -------
        bins : dict
             : bins[i] is a list of nodes in random order with exactly i stubs 
             : available. 
        freq : array_like
             : freq[max(D) - i] is the number of nodes with at least (max(D)-i) 
             : stubs that have yet to be allocated to subgraphs (i.e., a 
             : cumulative frequency count from the maximum degree down to zero). 
        """
        idx = np.arange(len(D))
        bins = {i: [] for i in range(0, D.max()+1)}
        for i, d in enumerate(D):
            bins[d].append(i)
            
        freq = [len(i) for i in bins.values()]

        return bins, freq

    def _select_accommodating_node(self, min_degree):
        """Selects a node with degree >= min_degree proportional to how many 
        nodes there are of a given degree. 
        Parameters
        ----------
        min_degree : int
                   : The total number of stubs for given corner configuration.
        """

        if self.remaining_stubs.max() < min_degree:
            raise ValueError(( 'The lower bound on desired stubs exceeds the '
                               'maximum available degree.') )
            sys.exit()
        else:
            freq = self.freq[min_degree:]
            total = sum(freq)
            p = [f/total for f in freq]
            choice = np.random.choice(np.arange(len(freq)), p=p) + min_degree
            if not self.bins[choice]:
                print("Choice: {}".format(choice))
                for k, v in self.bins.items():
                    print("Degree: {}, Freq: {}, Nodes: {}. \n ".format(k, self.freq[k]/sum(self.freq), v) )
            node = random.choice(self.bins[choice])
            self.bins[choice].remove(node)
            return node

    def _allocate_subgraphs_to_nodes(self):
        """
        """
        # Condition: every subgraph corner in each sequence has been allocated 
        # to a node. 
        def condition(x): return x.index<self._N

        while any(map(condition, self._subgraph_sequences)):
            corner, subgraph_index = self._select_corner()
            node = self._select_accommodating_node(sum(corner))
            self.maintain_counts(node, sum(corner))
            self._subgraph_sequences[subgraph_index].allocated_sequence[:,node] = corner
    
    def maintain_counts(self, node, stubs): 
        """
        """
        self.freq[self.remaining_stubs[node]] -= 1
        self.remaining_stubs[node] -= stubs
        self.bins[self.remaining_stubs[node]].append(node)
        self.freq[self.remaining_stubs[node]] +=1 

            
    def _select_corner(self): 
        """Select a corner at random.
        """
        choice = np.random.choice(len(self._subgraph_sequences))
        return self._subgraph_sequences[choice].get_corner(), choice 
