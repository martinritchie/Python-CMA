import ipdb
import networkx as nx
import numpy as np
import random
def CMA(D, subgraphs, subgraphSeq):
    # --------------------------- - Input - ----------------------------------
    # D: degree sequence
    # subgraphs: subgraphs to be included (list of subgraphs, see subgraph.py)
    # subgraphSeq: subgraph sequences (list of lists)
    # ---------------------- - Constraints on input - ------------------------
    # 1. The degree sequence must sum to an even number.
    # 2. Each subgraph sequence must sum to a number that is divisible by the 
    #    number of nodes in the corresponding subgraph.
    # ---------------------------- - Output - --------------------------------
    # A: a networkx graph. 
    # ------------------------ - Example call - ------------------------------
    # See CMAtestCases.py for various examples. 
    # ----------------------------- - Notes - --------------------------------
    # For incomplete subgraphs the subgraphs must be enumerated so that corners 
    # of the same type are represented by adjacent integers see the following toast for example:  
    #       toast = subGraph([(0, 2), (0, 3), (2, 3), (1, 2), (1, 3)])
    # The ordering is essential to the connection process. 
    # ------------------------- - Key variables - ----------------------------
    N = len(D)
    d = list(D) 

    # hStubTup, hyperstub tuples. Each element of the list, hStubTup, is a  
    # sequence of length N of tuples(including 1-tuples). There is one list of 
    # tuples per subgraph. The tuples size corresponds to the number of corner 
    # types of the sequences' subgraphs. The value of these tuples is decided 
    # multinomially for 2-tuples or greater. The values represent the classical 
    # stub count of the hyperstub. The tuples have not yet been allocated to 
    # subgraphs.
    hStubTup = []

    # tupInducedD, tuple induced degree. Each element of the list, tupInducedD, 
    # is an integer sequence. There is one such sequence per subgraph. Each 
    # sequence is computed by summing the tuples in the associated
    # hStubTup sequence. This sum denotes minimum degree required for a
    # particular hyperstub configuration.
    tupInducedD = []

    # sSeq, subgraph sequences. A list of sequences contain the corner count(s) 
    # for a particular subgraph. For incomplete subgraphs this will be tuple. 
    sSeq = []
    
    # OsSeq, ordered subgraph sequences. An ordered version of sSeq, i.e, index 
    # i of a particular sequence corresponds to the corner types incident to 
    # node i. 
    OsSeq = []
    # H, hyperstub sequences. The same as OsSeq but the counts are multiplied by 
    # their stub cardinality. 
    H = []

    # --------------------------- - Preprocessing - ---------------------------
    # The following for loop determines the stub degree of induced by a particular subgraph count as well as decomposes the counts into hyperstub types for incomplete subgraphs. All of the sequences in this loop are unordered, i.e., have not been allocated to nodes. 
    for i, sub in enumerate(subgraphs):
        # for subgraphs with a single corner type...
        if len(sub.cornerTypes()) == 1:
            sSeq.append(subgraphSeq[i])
            corners = sub.cornerTypes()
            hStubTup.append([subgraphSeq[i][j] * corners[0] for j in xrange(N)])
            tupInducedD.append(hStubTup[-1])
            # Initialising.
            H.append([0 for x in xrange(N)])
            OsSeq.append([0 for x in xrange(N)])
        else:
            hstubtypes =  len(sub.cornerTypes())
            temp = [0] * hstubtypes
            p = sub.cornerProportion()
            # Split the sequence for incomplete subgraphs.   
            sSeq.append(incomSubSeq(subgraphSeq[i], p))
            corners = sub.cornerTypes()
            # Compute the decomposed tuples' classic degree.
            temp = np.multiply(sSeq[-1], np.transpose([corners] * N))
            sSeq[-1] = zip(*sSeq[-1])
            hStubTup.append(zip(*temp))
            # Sum to get a lower bound on the degree for potential accommodating nodes.
            temp = np.sum(np.array(temp), 0)
            tupInducedD.append(temp.tolist())
            temp = []
            # Initialising.
            H.append([(0,)*hstubtypes for x in xrange(N)])
            OsSeq.append([(0,)*hstubtypes for x in xrange(N)])
    
    # ------------------------------- - CMA - ---------------------------------
    # The following while loop allocated subgraphs to nodes. The sequences created by this loop are ordered, i.e., index i will correspond to a node i. 
    # totals: the number of remaining hyperstubs to be
    # allocated to nodes (stop condition)
    totals = sum(map(sum, tupInducedD))
    # usedNodes: a node is elegible for selection once for a given subgraph sequence. This keeps track of which nodes have been used. 
    usedNodes = np.zeros([len(subgraphs), N])
    while totals > 0:
        # maxSS: the largest induced classical degree from each hyperstub sequence. 
        maxSS = map(max, tupInducedD)
        # minDegree: minimal degree required for largest induced hyperstub(s)
        minDegree = max(maxSS)
        sIdx = maxSS.index(minDegree)
        # dIdx: the index from the subgraph sequence that requires the
        dIdx = tupInducedD[sIdx].index(maxSS[sIdx])                      
        # select candidate nodes (index) for the hyperstub(s)
        cNodes = [i for i in xrange(len(d)) if d[i] >= minDegree]
        try:
            node = random.choice(cNodes)
        except:
            print 'The degree sequence cannot accommodate the subgraph sequences'
            return 'reset', minDegree
        # If the selected node already has been allocated one of the given subgraphs a new node must be selected. 
        attempt = 0
        while usedNodes[sIdx][node] == 1 and attempt < 2*len(cNodes):
            node = random.choice(cNodes)
            attempt +=1
        if attempt ==  2*len(cNodes):
            return 'reset'
        # Allocate the subgraph degree to H
        H[sIdx][node] = hStubTup[sIdx][dIdx]
        OsSeq[sIdx][node] = sSeq[sIdx][dIdx]
        # Update counters and sequences.
        tupInducedD[sIdx][dIdx] = 0
        d[node] = d[node] - minDegree
        usedNodes[sIdx][node] = 1
        totals -= minDegree
    # ------------------ - Connection Process - --------------------
    # Initialise the network,
    A = nx.Graph()
    # with N nodes. 
    A.add_nodes_from(list(xrange(N)))
    
    # First all subgraphs are connected
    for s, sub in enumerate(subgraphs):
        # Inialise and compute key variables
        hStubBins = []
        # the number of different hyperstub for the given subgraph
        hstubtypes = len(sub.cornerTypes())
        size_of_s = sub.number_of_nodes()
        s_current_edges = sub.edges()
        # the number of each hyperstub count found in the given subgraph
        cQuantities = sub.cornerQuantities()
        
        for i in xrange(hstubtypes):
            hStubBins.append([])
        
        # populate the bins 
        for i in xrange(N):
            if isinstance( OsSeq[s][i], int ):
                sDegree = [OsSeq[s][i]]
            else:
                sDegree = list(OsSeq[s][i])
            for j in xrange(hstubtypes):
                for k in range(sDegree[j]):
                    hStubBins[j].append(i)
        
        # randomise the bins
        for i in range(hstubtypes): 
            random.shuffle(hStubBins[i]) 
        attempt = 0
        reset = 0

        while sum(map(sum,hStubBins))>0:
            nodes = [] 
            a = A.subgraph(nodes)
            node_duplicates = len(set(nodes)) != size_of_s
            # current_edges is used to check for double edges. 
            current_edges = len(a.edges())
            
            while node_duplicates or current_edges > 0: 
                # Make a selection of nodes from the bins
                for i in range(hstubtypes):
                    for j in range(cQuantities[i]):
                        # The order of nodes is important.
                        nodes.append(hStubBins[i].pop())
                node_duplicates = len(set(nodes)) != size_of_s
                a = A.subgraph(nodes)
                current_edges = len(a.edges())
                # If the selection results in an artifact edge return the nodes to thier original bins and reshuffle. 
                if node_duplicates or current_edges > 0:
                    for i in range(hstubtypes):
                        for j in range(cQuantities[i]):
                            hStubBins[i].append(nodes.pop(0))
                        random.shuffle(hStubBins[i]) 
                    attempt +=1
                    # Condition to stop dead end configurations, e.g., many of the same node left in one bin.  
                    if attempt > len(hStubBins[0]):
                        return 'reset' 
            for i in range(size_of_s):
                for j in range(size_of_s): 
                    if (i,j) in s_current_edges:
                        A.add_edge(nodes[i],nodes[j])
        bag = []   
    for i in range(N):
        for j in range(d[i]):
            bag.append(i)
    random.shuffle(bag)
    while bag:
        u = bag.pop()
        v = bag.pop()
        attempt = 0 
        while u==v or A.has_edge(u, v):
            bag.insert(0, v)
            v = bag.pop()
            attempt += 1 
            if attempt>len(bag):
                random.shuffle(bag)
                reset +=1

            if reset ==5:
                return 'reset'
        A.add_edge(u,v)
    return A

def CMA_reset(D, subgraphs, subgraphSeq):
    A = 'reset'
    counter = 0
    while A == 'reset' and counter < 100:
        A = CMA(D, subgraphs, subgraphSeq)
        counter +=1
    if counter == 100:
        return 'reset'
    return A 

def triangles(A):
    #returns the number of triangles, tri, and global clustering coefficient, 1.0*tri/trip. 
    A = nx.to_numpy_matrix(A)
    A2 = np.dot(A,A)
    A3 = np.dot(A2,A)
    tri = np.trace(A3)
    trip = np.sum(np.sum(A2)) - tri
    return tri, 1.0*tri/trip

def incomSubSeq(s,p):
    # for an input sequence, s, and vector of probabilities this function returns a matrix with column i determined by the multinomial distribution with parameters s(i) and p. 
    if sum(s) == 0:
        return np.zeros([len(p), len(s)])
    total = 1
    totals =  np.zeros(len(p))
    p = np.array(p)
    while not (1.0*totals/total==p).any():
        S = np.zeros([len(p), len(s)],dtype=int)
        totals =  np.zeros(len(p))
        for i in range(len(s)):
            S[:,i] = np.random.multinomial(s[i], p, size=1)
            totals += S[:,i]
        total = sum(totals)
    return S

def degreeSequence(A):
    D = np.zeros(len(A.nodes()),dtype=int)
    for edge in A.edges():
        D[edge[0]] += 1
        D[edge[1]] += 1
    return D 