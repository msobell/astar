#! /usr/bin/env python
"""
Usage: %s <number N>

Solves the Astar problem (http://cs.nyu.edu/courses/fall10/G22.2965-001/)
"""
import os
import sys
import time
import math

class Edge:
    """A class to keep track of edges"""
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2
        ## REMEMBER TO TAKE THE SQRT AT THE END!
        self.dist2 = (v1.x - v2.x)**2 + (v1.y - v2.y)**2 + (v1.z - v2.z)**2

    def __repr__(self):
        return "v1: %s \tv2: %s \tdist2: %s" % (repr(self.v1), repr(self.v2), repr(self.dist2))

    def __cmp__(self,e2):
        return self.dist2 - e2.dist2

    def realDist(self):
        return math.sqrt(self.dist2)

class Vertex:
    def __init__(self,n,x,y,z):
        self.n = n #number
        self.x = x
        self.y = y
        self.z = z
        self.degree = 0

    def __repr__(self):
        return "%s\tx: %s\ty: %s\tz: %s" % (repr(self.n), repr(self.x), repr(self.y), repr(self.z))

start_time = time.time()
POINTS = 1000
vertices = []
edges = []

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

def minimumSpanningTree():
    mst_vertices = []
    mst = []
    for edge in edges:
        if not (edge.v1 in mst_vertices and edge.v2 in mst_vertices):
            edge.v1.degree += 1
            edge.v2.degree += 1
            mst_vertices.append( edge.v1 )
            mst_vertices.append( edge.v2 )
            mst.append( edge )
        if len(mst_vertices) == POINTS:
            break
    return mst,len(mst),sum([edge.dist2 for edge in mst])

def minimumMatching(mst):
    odd_vertices = []

    for v in vertices:
        if v.degree % 2:
            odd_vertices.append(v)

    print "Odd vertices:\t" + repr(len(odd_vertices))

    for e in edges:
        if e.v1 in odd_vertices and e.v2 in odd_vertices:
            mst.append( e )
            odd_vertices.remove(e.v1)
            odd_vertices.remove(e.v2)

    return mst

def printTime():
    print "Time:\t\t" + repr(round(time.time() - start_time,4))
        
if __name__ == "__main__":

    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

    # read in and create vertex objects
    for line in sys.stdin:
        a = line.split()
        vertices.append(Vertex(int(a[0]),int(a[1]),int(a[2]),int(a[3])))

    for v1 in vertices:
        for v2 in vertices[v1.n:]:
            # only up to highest done in outer
            if v1.n == v2.n:
                pass
            else:
                edges.append(Edge(v1,v2))

    # sort the edges by distance
    edges = sorted(edges, key=lambda Edge: Edge.dist2)
    # much slower:
    # edges.sort()

    mst = minimumSpanningTree()

    print "MST edges:\t" + repr(mst[1])
    print "MST length:\t" + repr(round(math.sqrt(mst[2]),2))

    printTime()

    mmst = minimumMatching(mst[0])

    print "M MST edges:\t" + repr(len(mmst))
    print "M MST length:\t" + repr(round(math.sqrt(sum([edge.dist2 for edge in mmst])),2))
        
    printTime()

    # now we have a path to follow!
