import os, random
from graph import DiGraph
import algorithms
from copy import deepcopy,copy
import global_route_with_tm_bound as common
import paper_cplex_input_without_tm as cplex
import utilization_from_route as utils
import parse_xml as xml
from deep_first_search_path import *

def adjust_route(topology, remove_file, routes, link_order):
    # get remove_links
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

    # get final topology
    g = DiGraph()
    f = open(topology)
    line = f.readline()
    line = f.readline()
    while line:
        s = line.rstrip().split(' ')
        lls = int(s[0])
        lld = int(s[1])

        #g.add_nodes([int(s[0]), int(s[1])])
        g.add_edge(lls, lld, link_order[lls,lld][1] / link_order[lls,lld][0])
        g.add_edge(lld, lls, link_order[lls,lld][1] / link_order[lls,lld][0])

        line = f.readline()
    f.close()

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

    for ls,ld in links:
        #print(ls,ld)
        for s,d in routes:
            route_paths = routes[s,d]

            remove_route = []
            remove_weight = 0
            for path, weight in route_paths:
                for i in range(len(path) - 1):
                    if (path[i] == ls and path[i+1] == ld) or (path[i] == ld and path[i+1] == ls):
                        remove_route.append([path, weight])
                        remove_weight += weight

                        # remove weight from all the link
                        for pi in range(len(path) - 1):
                            ps = path[pi]
                            pd = path[pi+1]
                            if pd < ps:
                                tmp = pd
                                pd = ps
                                ps = tmp

                            link_order[ps,pd][1] -= weight

                        break
            if remove_weight != 0:
                # Find k-shortest-paths between s,d
                tmp_paths = algorithms.ksp_yen(g, s, d, 20)
                yen_paths = [[yen_path['path'], 0, 0] for yen_path in tmp_paths]
                
                # make sure the proportion of every yen_path
                steps = 10.0
                gap = remove_weight / steps
                calculate_cf(yen_paths, link_order)
                for step in range(int(steps)):
                    for yi in range(len(yen_paths[0][0]) - 1):
                        ys = yen_paths[0][0][yi]
                        yd = yen_paths[0][0][yi + 1]
                        if yd < ys:
                            tmp = ys
                            ys = yd
                            yd = tmp
                        link_order[ys,yd][1] += gap
                    yen_paths[0][2] += 1 / steps
                    calculate_cf(yen_paths, link_order)

                # remain routes
                for rr in remove_route:
                    route_paths.remove(rr)

                # merge k-s-p into routes
                for yen_path, flows, proportion in yen_paths:
                    if proportion == 0:
                        continue

                    exist = False
                    for rp in route_paths:
                        if rp[0] == yen_path:
                            rp[1] += remove_weight * proportion
                            exist = True
                    if not exist:
                        route_paths.append([yen_path, remove_weight * proportion])

                routes[s,d] = route_paths
    
    return routes

def fixed_route(routes):
    for s,d in routes:
        paths = deepcopy(routes[s,d])
        random_num = random.uniform(0, 1)
        for p,w in paths:
            if random_num < w:
                routes[s,d] = [[p, 1]]
                break
            else:
                random_num -= w

    return routes

def check_route_in_detail(routes, link_order, removes):
    for s,d in routes:
        paths = routes[s,d]
        weight = 0
        for path, w in paths:
            if path[0] != s:
                print Wrong
            for i in range(len(path) - 1):
                ls = path[i]
                ld = path[i+1]
                if ls > ld:
                    tmp = ls
                    ls = ld
                    ld = tmp
                if (ls, ld) not in link_order or (ls, ld) in removes:
                    print "Wrong"
            if path[len(path) - 1] != d:
                print "Wrong"
            weight += w

        #if weight != 1:
        #    print weight
            
def check_route(routes, link_order):
    for s,d in routes:
        path = routes[s,d][0][0]
        if path[0] != s:
            print Wrong
        for i in range(len(path) - 1):
            ls = path[i]
            ld = path[i+1]
            if ls > ld:
                tmp = ls
                ls = ld
                ld = tmp
            if (ls, ld) not in link_order:
                print "Wrong"
        if path[len(path) - 1] != d:
            print "Wrong"



if __name__ == '__main__':
    #topology = '../topology/final/geant-final-topology-12-base'
    topology_base = '../topology/final/geant-final-topology-15-base'
    #solutions = 'abilene-connected-cplex.xml'
    solutions = 'geant-connected-cplex.xml'
    routes = xml.get_route(solutions)
    remove_file_base = '../topology/remove/geant-remove-12-links-base'
    #remove_file = '../topology/remove/abilene-remove-4-links'
    demand_file = '../demand/gravity-abilene/1000.txt'
    f = open(remove_file_base)
    removes = []
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

        removes.append((ls,ld))
        removes.append((ld,ls))
        line = f.readline()
    f.close()

    topology_connect = '../topology/connected/geant-connected-topology'
    link_order = xml.get_link_order_with_attr(solutions, topology_connect)
    
    #min_routes = xml.get_route_with_demand("1_min_abilene_cplex.xml", demand_file)
    #min_routes = xml.get_route_with_demand("min_cplex_output.xml", demand_file)
    #print utils.get_utilization_with_probability(topology_connect, min_routes, 1)

    #print xml.get_link_order(solutions, topology_connect)

    #route = fixed_route(adjust_route(topology, remove_file, routes, link_order))
    check_route_in_detail(routes, link_order, [])

    routes_copy = deepcopy(routes)
    link_order_copy = deepcopy(link_order)
    route = adjust_route(topology_base, remove_file_base, routes_copy, link_order_copy)
    #print route
    #print common.global_utilization(topology_base, route, demand_file, 1) 

    #routes_copy = deepcopy(routes)
    #link_order_copy = deepcopy(link_order)
    #route = adjust_route(topology, remove_file, routes_copy, link_order_copy)
    #print route
    #print common.global_utilization(topology, route, demand_file, 1) 
    
    #check_route_in_detail(route, link_order, removes)
