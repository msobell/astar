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
        self.n = n
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "%s\tx: %s\ty: %s\tz: %s" % (repr(self.n), repr(self.x), repr(self.y), repr(self.z))

start_time = time.time()
POINTS = 1000
vertices = []
edges = []

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

def MinimumSpanningTree():
    mst_vertices = []
    mst = []
    for edge in edges:
        if not (edge.v1 in mst_vertices and edge.v2 in mst_vertices):
            mst.append( edge )
        if len(mst_vertices) == POINTS:
            break
    return mst,len(mst),sum([edge.dist2 for edge in edges])
        
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

    mst = MinimumSpanningTree()

    print "MST edges:\t" + repr(mst[1])
    print "MST length:\t" + repr(mst[2])
    
    print "Time:\t\t" + repr(time.time() - start_time)
