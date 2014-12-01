import os, random
from copy import deepcopy
import paper_cplex_input_without_tm as cplex
import utilization_from_route as utils
import parse_xml as xml
from deep_first_search_path import *

def adjust_route(topology, remove_file, routes, link_order):
    f = open(remove_file)
    links = []
    line = f.readline()
    while line:
        s = line.rstrip().split(' ')
        s = [int(i) for i in s]
        
        ls = s[0]
        ld = s[1]
        if ld < ls:
            tmp = ls
            ls = ld
            ld = tmp

        links.append((ls,ld))
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
        path_replace[ls,ld] = g.find_path_without_weight(ls,ld)

    #print path_replace
    #print link_order
    
    def sort_path(paths):
        for i in range(len(paths)):
            for j in range(i, len(paths)):
                if paths[i][1] < paths[j][1]:
                    tmp = paths[i]
                    paths[i] = paths[j]
                    paths[j] = tmp

    def calculate_cf(paths, link_order):
        for p in paths:
            cf = 100000
            for i in range(len(p[0]) - 1):
                tmp_cf = 0
                s = p[0][i]
                d = p[0][i+1]
                if s < d:
                    tmp_cf = link_order[s,d][0] / link_order[s,d][1]
                else:
                    tmp_cf = link_order[d,s][0] / link_order[d,s][1]
                if tmp_cf < cf:
                    cf = tmp_cf
            p[1] = cf
            sort_path(paths)

    for (ls,ld) in path_replace:
        paths = path_replace[ls,ld]
        calculate_cf(paths, link_order)

    for (ls,ld) in path_replace:
        paths = path_replace[ls,ld]
        flows = link_order[ls,ld][1]

        GAP_NUM = 10
        gap = flows / GAP_NUM
        used = 0
        for loop in range(GAP_NUM):
            #do something
            for i in range(len(paths[0][0]) - 1):
                s = paths[0][0][i]
                d = paths[0][0][i+1]

                if d < s:
                    tmp = s
                    s = d
                    d = tmp

                link_order[s,d][1] += gap
            paths[0][2] += 0.1
            calculate_cf(paths, link_order)
            #print paths
            #print used
            used += gap

        path_replace[ls,ld] = paths

    
    select_path = []
    for ls,ld in links:
        #print(ls,ld)
        for s,d in routes:
            for i in range(len(routes[s,d])):
                for j in range(len(routes[s,d][i][0]) - 1):
                    if routes[s,d][i][0][j] == ls and routes[s,d][i][0][j+1] == ld:
                        random_num = random.uniform(0, 1)
                        for p in path_replace[ls, ld]:
                            if random_num < p[2]:
                                select_path = deepcopy(p[0])
                                break
                            else:
                                random_num -= p[2]

                        if path_replace[ls, ld] != None:
                            routes[s,d][i] = [routes[s,d][i][0][0:j] + select_path + routes[s,d][i][0][j+2:], routes[s,d][i][1]]
                        else:
                            print("Wrong")
                        break

                    elif routes[s,d][i][0][j] == ld and routes[s,d][i][0][j+1] == ls:
                        random_num = random.uniform(0, 1)
                        for p in path_replace[ls, ld]:
                            if random_num < p[2]:
                                select_path = deepcopy(p[0])
                                break
                            else:
                                random_num -= p[2]

                        select_path.reverse()
                        if path_replace[ls, ld] != None:
                            routes[s,d][i] = [routes[s,d][i][0][0:j] + select_path + routes[s,d][i][0][j+2:], routes[s,d][i][1]]
                        else:
                            print("Wrong")
                        break

    
    return routes

if __name__ == '__main__':
    topology = '../topology/final/abilene-final-topology-1'
    routes = xml.get_route('abilene-connected-cplex.sol')
    remove_file = '../topology/remove/abilene-remove-1-links'

    topology_connect = '../topology/connected/abilene-connected-topology'
    solutions = 'abilene-connected-cplex.sol'
    link_order = xml.get_link_order_with_attr(solutions, topology_connect)

    adjust_route(topology, remove_file, routes, link_order)
