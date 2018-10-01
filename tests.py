# Written by M.Ritchie, September 2018. 
import numpy as np
from subgraphs import subGraphSequence
from subgraphs import subGraph
import unittest 
from scipy import stats 

def triangle():
    """Three nodes that share every possible connection. 
    """
    G = subGraph()
    G.add_edges_from([ (0,1),
                       (1,2),
                       (0,2) ])
    return G

def toast():
    """Four nodes, two triangles. Looks like toast cut from corner to corner. 
    """
    G = subGraph()
    G.add_edges_from([ (0,1), 
                       (1,2),
                       (2,3),
                       (3,0),
                       (0,2) ])
    return G

class subgraphTests(unittest.TestCase):
    """Tests the basic functionality of subgraphs.subGraph.
    """

    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)

        self.triangle = triangle() 
        self.toast    = toast()

    def test_triangle_degree_sequence(self):
        self.assertEqual(self.triangle.D, [2, 2, 2])

    def test_triangle_edge_count(self):
        self.assertEqual(self.triangle.m, 6)

    def test_triangle_corner_types(self):
        self.assertEqual(self.triangle.cornerTypes, [2])

    def test_triangle_corner_dist(self):
        self.assertEqual(self.triangle.cornerDist, [1])
        
    def test_triangle_corner_counts(self):
        self.assertEqual(self.triangle.cornerCounts, {2:3} )

    def test_toast_degree_sequence(self):
        self.assertEqual(self.toast.D, [3, 2, 3, 2])

    def test_toast_edge_count(self):
        self.assertEqual(self.toast.m, 10)

    def test_toast_corner_types(self):
        self.assertEqual(self.toast.cornerTypes, [2, 3])

    def test_toast_corner_dist(self):
        self.assertEqual(self.toast.cornerDist, [1/2, 1/2])
        
    def test_toast_corner_counts(self):
        self.assertEqual(self.toast.cornerCounts, {2:2, 3:2} )


class subgraphSequenceTests(unittest.TestCase):
    """Tests the basic functionality of subgraphs.subGraphSequence.
    """

    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)

        triangle_sequence = np.ones((6,), dtype=int)
        triangle_subgraph = triangle()
        self.Triangle = subGraphSequence(triangle_sequence, triangle_subgraph)

        toast_sequence = np.ones((10000,), dtype=int)
        toast_subgraph = toast()
        self.Toast = subGraphSequence(toast_sequence, toast_subgraph)

    def test_tri_resolvedPositions(self):
        rp   = self.Triangle.resolvedPositions
        test =  np.ones((6,), dtype=int)
        self.assertTrue( (rp==test).all() )
    
    def test_tri_totalstubs(self):
        ts   = self.Triangle.totalStubs
        test =  np.ones((6,), dtype=int)*2
        self.assertTrue( (ts==test).all() )

    def test_toast_resolvedPositions(self): 
        RV = self.Toast.resolvedPositions
        RV = np.sum(RV, axis=0)
        _, p = stats.chisquare(RV, [5000, 5000])
        self.assertTrue( 0.01 < p )

    def test_toast_totalstubs(self): 
        ts   = self.Toast.totalStubs
        twos = np.sum([i for i in ts if i==2])
        thre = np.sum([i for i in ts if i==3])
        _, p = stats.chisquare([twos, thre], [2*5000, 3*5000])
        self.assertTrue( 0.01 < p )




if __name__ == '__main__':
    unittest.main()