from subGraph import * 
from CMA import *
#from CMA import * 
# Subgraph objects inherit thier properties from network x's 'graphl,
# see subGraph.py
# Initialise subgraphs:
line = subGraph([(0, 1)])
triangle = subGraph([(0, 1), (1, 2), (2, 0)])
eSquare = subGraph([(0, 1), (1, 2), (2, 3), (0, 3)])
toast = subGraph([(0, 2), (0, 3), (2, 3), (1, 2), (1, 3)])
cSquare = subGraph([(0, 1), (1, 2), (2, 3), (0, 3), (1, 3), (0, 2)])
dPent = subGraph([(0, 1), (1, 2), (2, 3), (3, 4),
                  (0, 1), (0, 2), (0, 3), (0, 4)])

# -----------------------------------------------------------------
#						   CMA TEST CASES
# -----------------------------------------------------------------
# The number of test cases
num_cases = 5

print 'Case 1: homogeneous configuration models networks...'
for i in range(num_cases):
	N = 1000
	D = [5] * N
	sub = 0
	Sub = [0]*N
	Sub[0:sub] = [1]*sub

	subgraphs = [triangle]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)

	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 1 failed, degree sequence.'
		break

	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri/6.0 < sum(Sub)*triangle.triangleAverage():
		print 'Case 1 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % sum(Sub)*triangle.triangleAverage()
		print 'Actual triangles: %d' %  Atri/6.0
		break
if i == num_cases-1:
	print 'Case 1: passed.'

# -----------------------------------------------------------------

print 'Case 2: heterogeneous configuration models networks...'
for i in range(num_cases):
	N = 1000
	D =  np.random.poisson(5, N)
	while sum(D) % 2 != 0:
		D =  np.random.poisson(5, N)
	sub = 0
	Sub = [0]*N
	Sub[0:sub] = [1]*sub

	subgraphs = [triangle]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)

	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 2 failed, degree sequence.'
		break

	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri/6.0 < sum(Sub)*triangle.triangleAverage():
		print 'Case 2 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % sum(Sub)*triangle.triangleAverage()
		print 'Actual triangles: %d' %  Atri/6.0
		break
if i == num_cases-1:
	print 'Case 2: passed.'

# -----------------------------------------------------------------

print 'Case 3: very heterogeneous configuration models networks...'
for i in range(num_cases):
	N = 1000
	D = np.random.geometric(p=0.2, size=N)
	while sum(D) % 2 != 0:
		D = np.random.geometric(p=0.2, size=N)
	sub = 0
	Sub = [0]*N
	Sub[0:sub] = [1]*sub

	subgraphs = [triangle]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)

	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 3 failed, degree sequence.'
		break

	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri/6.0 < sum(Sub)*triangle.triangleAverage():
		print 'Case 3 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % sum(Sub)*triangle.triangleAverage()
		print 'Actual triangles: %d' %  Atri/6.0
		break
if i == num_cases-1:
	print 'Case 3: passed.'

# -----------------------------------------------------------------

print 'Case 4: homogeneous configuration models networks with:'
print 'homogeneous triangles...'
for i in range(num_cases):
	N = 1000
	D = [5] * N
	sub = 900
	Sub = [0]*N
	Sub[0:sub] = [1]*sub

	subgraphs = [triangle]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)

	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 4 failed, degree sequence.'
		break

	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri/6.0 < sum(Sub)/3.0:
		print 'Case 4 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % sum(Sub)*triangle.triangleAverage()
		print 'Actual triangles: %d' %  Atri/6.0
		break
if i == num_cases-1:
	print 'Case 4: passed.'

# -----------------------------------------------------------------

print 'Case 5: homogeneous configuration models networks with:'
print 'every edge part of a triangle...'
for i in range(num_cases):
	N = 900
	D = [4] * N
	sub = 900
	Sub = [0]*N
	Sub[0:sub] = [2]*sub

	subgraphs = [triangle]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)
	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 5 failed, degree sequence.'
		break

	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri/6.0 < sum(Sub)/3.0:
		print 'Case 5 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % sum(Sub)*triangle.triangleAverage()
		print 'Actual triangles: %d' %  Atri/6.0
		break
if i == num_cases-1:
	print 'Case 5: passed.'

# -----------------------------------------------------------------

print 'Case 6: homogeneous configuration models networks with:'
print 'homogeneous complete squares...'
for i in range(num_cases):
	N = 1000
	D = [5] * N
	sub = 800
	Sub = [0]*N
	Sub[0:sub] = [1]*sub

	subgraphs = [cSquare]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)

	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 6 failed, degree sequence.'
		break

	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri/6.0 < sum(Sub)/3.0:
		print 'Case 6 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % sum(Sub)*triangle.triangleAverage()
		print 'Actual triangles: %d' %  Atri/6.0
		break

if i == num_cases-1:
	print 'Case 6: passed.'

# -----------------------------------------------------------------

print 'Case 7: homogeneous configuration models networks with:'
print 'homogeneous empty squares...'
for i in range(num_cases):
	N = 1000
	D = [5] * N
	sub = 800
	Sub = [0]*N
	Sub[0:sub] = [2]*sub

	subgraphs = [eSquare]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)

	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 7 failed, degree sequence.'
		break

	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri/6.0 < 0:
		print 'Case 7 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % sum(Sub)*eSquare.triangleAverage()
		print 'Actual triangles: %d' %  Atri/6.0
		break

if i == num_cases-1:
	print 'Case 7: passed.'

# -----------------------------------------------------------------

print 'Case 8: homogeneous configuration models networks with:'
print 'mostly toast...'
for i in range(num_cases):
	N = 1000
	D = [6] * N
	sub = 1000
	Sub = [0]*N
	Sub[0:sub] = [2]*sub

	subgraphs = [toast]
	subgraphSeq = [Sub]
	A = CMA_reset(D, subgraphs, subgraphSeq)
	if A[0] == 'reset':
	    break
	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 8 failed, degree sequence.'
		break


	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri < 12*2*sub/4.0:
		print 'Case 8 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % 12*2*sub/4.0
		print 'Actual triangles: %d' %  Atri/6.0
		break
if i == num_cases-1:
	print 'Case 8: passed.'

# ------------------------------------------------------------------

print 'Case 9: homogeneous configuration models networks with:'
print 'toast and triangles...'
for i in range(num_cases):
	N = 1000
	D = [5] * N
	
	sub1 = 999
	Sub1 = [0]*N
	Sub1[0:sub1] = [1]*sub1
	
	sub2 = 1000
	Sub2 = [0]*N
	Sub2[0:sub2] = [1]*sub2

	subgraphs = [triangle, toast]
	subgraphSeq = [Sub1, Sub2]
	A = CMA_reset(D, subgraphs, subgraphSeq)
	if A[0] == 'reset':
	    break
	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 9 failed, degree sequence.'
		break


	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri < 12*sub1/4.0 + 2*999:
		print 'Case 9 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % 12*sub1/4.0 + 2*999
		print 'Actual triangles: %d' %  Atri
		break
if i == num_cases-1:
	print 'Case 9: passed.'

# ------------------------------------------------------------------

print 'Case 10: heterogeneous configuration models networks with:'
print 'toast and triangles...'
for i in range(num_cases):
	N = 1000
	D = np.random.poisson(5, N)
	while sum(D) % 2 != 0:
		D =  np.random.poisson(5, N)
	sub1 = 99
	Sub1 = [0]*N
	Sub1[0:sub1] = [1]*sub1
	
	sub2 = 100
	Sub2 = [0]*N
	Sub2[0:sub2] = [1]*sub2

	subgraphs = [triangle, toast]
	subgraphSeq = [Sub1, Sub2]
	A = CMA_reset(D, subgraphs, subgraphSeq)
	if A[0] == 'reset':
	    break
	# Check the degree sequence 
	if not all(degreeSequence(A) == D):
		print 'Case 10 failed, degree sequence.'
		break


	# Check the number of triangles
	Atri, C = triangles(A)
	if Atri < sub1*2 + sub2*3:
		print 'Case 9 failed, fewer triangle than expected.'
		print 'Expected triangles: %d' % 12*sub1/4.0 + 2*999
		print 'Actual triangles: %d' %  Atri
		break
if i == num_cases-1:
	print 'Case 10: passed.'