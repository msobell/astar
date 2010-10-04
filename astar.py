#! /usr/bin/env python
"""
Usage: %s <number N>

Solves the Astar problem (http://cs.nyu.edu/courses/fall10/G22.2965-001/)
"""
import os
import sys
import time
import math
from UnionFind import UnionFind

class Edge:
    """A class to keep track of edges"""
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2
        ## REMEMBER TO TAKE THE SQRT AT THE END!
        self.dist2 = (v1.x - v2.x)**2 + (v1.y - v2.y)**2 + (v1.z - v2.z)**2
        self.visited = False

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
        self.order = -1

    def __repr__(self):
        return "%s\tx: %s\ty: %s\tz: %s\tdegree: %s" % (repr(self.n), repr(self.x), repr(self.y), repr(self.z), repr(self.degree))

start_time = time.time()
POINTS = 1000

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

def minimumSpanningTree(edges):
    subtrees = UnionFind()
    tree = []
    for e in edges:
        if subtrees[e.v1] != subtrees[e.v2]:
            tree.append(e)
            subtrees.union(e.v1,e.v2)
            e.v1.degree += 1
            e.v2.degree += 1
    return tree

    # mst_vertices = []
    # mst = []
    # for edge in edges:
    #     if not (edge.v1 in mst_vertices and edge.v2 in mst_vertices):
    #         edge.v1.degree += 1
    #         edge.v2.degree += 1
    #         mst_vertices.append( edge.v1 )
    #         mst_vertices.append( edge.v2 )
    #         mst.append( edge )
    #     if len(mst_vertices) == POINTS:
    #         break

def minimumMatching(mst):

    stillOdd = True

    while stillOdd:
        odd_vertices = []
        stillOdd = False
        for v in vertices:
            if (v.degree % 2) == 1:
                odd_vertices.append(v)
                stillOdd = True

        print "Odd vertices:\t" + repr(len(odd_vertices))

        for e in edges:
            if (e.v1 in odd_vertices) and (e.v2 in odd_vertices):
                mst.append( e )
                e.v1.degree += 1
                e.v2.degree += 1
                odd_vertices.remove( e.v1 )
                odd_vertices.remove( e.v2 )

    print "All degrees even!"
    return mst

def printTime():
    print "Time:\t\t" + repr(round(time.time() - start_time,4))
        
def make_stuff(edges, vertices):
    # read in and create vertex objects
    for line in sys.stdin:
        a = line.split()
        vertices.append(Vertex(int(a[0]),int(a[1]),int(a[2]),int(a[3])))

    # make edges from vertices
    for v1 in vertices:
        for v2 in vertices[v1.n:]:
            # only up to highest done in outer
            if v1.n == v2.n:
                pass
            else:
                edges.append(Edge(v1,v2))

    # sort the edges by distance
    return sorted(edges, key=lambda Edge: Edge.dist2),vertices
    # much slower:
    # edges.sort()

def euler(edges,vertices):
    visited_vertices = []
    edges = sorted(edges, key=lambda Edge: Edge.dist2)

    j = 0

    # arbitrary start
    v = vertices[0]

    while len(visited_vertices) < POINTS:
        # visit v
        v.order = j
        j += 1
        print "Vertex\t" + repr(v)
        v.degree -= 2
        if v.degree == 0:
            visited_vertices.append(v)
        # error!
        elif v.degree < 0:
            print v
            print "Whoops..."
            break
        # find the attached v
        for e in edges:
            if e.v1 == v and not e.visited:
                e.visited = True
                print "Edge\t" + repr(e)
                v = e.v2
                break
            elif e.v2 == v and not e.visited:
                e.visited = True
                print "Edge\t" + repr(e)
                v = e.v1
                break
                
            

if __name__ == "__main__":

    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

    vertices = []
    edges = []

    # make edges, vertices from input
    edges,vertices = make_stuff(edges, vertices)

    # create a MST
    mst = minimumSpanningTree(edges)

    print "MST edges:\t" + repr(len(mst))
    print "MST length:\t" + repr(round(math.sqrt(sum([e.dist2 for e in mst]))))

    printTime()

    # create a graph with vertices of even degree using minimum matchin
    mmst = minimumMatching(mst)

    print "M MST edges:\t" + repr(len(mmst))
    print "M MST length:\t" + repr(round(math.sqrt(sum([e.dist2 for e in mmst])),2))
        
    printTime()

    # now we have a multigraph that is at most 3/2 of the min so we number the vertices
    # to create an euler cycle

    print "Creating Euler Cycle"
    euler_cycle = euler(mmst,vertices)
    
    printTime()
