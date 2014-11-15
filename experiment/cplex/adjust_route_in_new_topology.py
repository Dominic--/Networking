import os
import paper_cplex_input_without_tm as cplex
import utilization_from_route as utils
import parse_xml as xml

def adjust_route(remove_file, routes):
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

    for ls,ld in links:
        #print(ls,ld)
        for s,d in routes:
            for i in range(len(routes[s,d])):
                for j in range(len(routes[s,d][i][0]) - 1):
                    if routes[s,d][i][0][j] == ls and routes[s,d][i][0][j+1] == ld:
                        weight = 0
                        index = 0
                        for k in range(len(routes[ls,ld])):
                            if routes[ls,ld][k][1]> weight:
                                index = k
                                weight = routes[ls,ld][k][1]
                        routes[s,d][i] = [routes[s,d][i][0][0:j] + routes[ls,ld][k][0] + routes[s,d][0][j+2:], routes[s,d][i][1]]

    return routes
