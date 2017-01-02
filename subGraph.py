import networkx as nx
import numpy as np

class subGraph(nx.Graph):

    def complete(self):
    	n = self.number_of_nodes()
    	s = self.size()
    	if n * (n - 1) / 2 == s:
    	    return 1
    	else:
    		return 0

    def degreeSequence(self):
        return list(self.degree().values())

    def cornerTypes(self):
    	return list(set(self.degreeSequence()))

    def cornerProportion(self):
    	ds = self.degreeSequence()
    	mds = max(ds)
    	dist = np.histogram(ds, bins=range(1, mds + 2), density=True)
        return filter(lambda a: a != 0.0, dist[0])

    def cornerQuantities(self):
        ds = self.degreeSequence()
        mds = max(ds)
        dist =  np.histogram(ds, bins=range(1,mds+2),density = False)
        return  filter(lambda a: a != 0.0, dist[0]) 

    def triangleAverage(self):
        A = nx.to_numpy_matrix(self)
        A2 = A*A
        A3 = A2*A
        return  np.trace(A3)/(self.number_of_nodes()*2.0)



