import os
import paper_cplex_input_without_tm as cplex
import utilization_from_route as utils
import parse_xml as xml
from deep_first_search_path import *

def adjust_route(topology, remove_file, routes):
    f = open(remove_file)
    links = []
    line = f.readline()
    while line:
        s = line.rstrip().split(' ')
        s = [int(i) for i in s]
        
        links.append((s[0],s[1]))
        links.append((s[1],s[0]))
        line = f.readline()
    f.close()
    
    g = Graph()
    f = open(topology)
    line = f.readline()
    line = f.readline()
    while line:
        s = line.rstrip().split(' ')

        g.add_nodes([int(s[0]), int(s[1])])
        g.add_edge((int(s[0]), int(s[1]), float(s[2])))
        g.add_edge((int(s[1]), int(s[0]), float(s[2])))

        line = f.readline()
    f.close()

    path_replace = dict()
    for ls,ld in links:
        path_replace[ls,ld] = g.dfs_path(ls,ld)

    #print(path_replace)

    for ls,ld in links:
        #print(ls,ld)
        for s,d in routes:
            for i in range(len(routes[s,d])):
                for j in range(len(routes[s,d][i][0]) - 1):
                    #print("ls, ld : %d %d" % (ls, ld))
                    #print("len : %d, j : %d" % (len(routes[s,d][i][0]), j))
                    if routes[s,d][i][0][j] == ls and routes[s,d][i][0][j+1] == ld:
                        '''
                        weight = 0
                        index = 0
                        for k in range(len(routes[ls,ld])):
                            if routes[ls,ld][k][1]> weight:
                                index = k
                                weight = routes[ls,ld][k][1]
                        '''
                        if path_replace[ls, ld] != None:
                            routes[s,d][i] = [routes[s,d][i][0][0:j] + path_replace[ls, ld] + routes[s,d][i][0][j+2:], routes[s,d][i][1]]
                        else:
                            routes[s,d][i] = [g.dfs_path(s, d), routes[s,d][i][1]]
                        break

    return routes
