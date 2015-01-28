import matplotlib.pyplot as plt
from copy import deepcopy
from prioritydictionary import priorityDictionary
from graph import DiGraph
import parse_xml as xml
import optimal_route_with_tm as optimal
import global_route_with_tm_bound as common
import new_adjust_route_in_new_topology as adjust

# Generate performance 

is_gravity = True
type_random = "bimodal"

connected_topology_template = "../topology/connected/%s-connected-topology"
final_topology_template = "../topology/final/%s-final-topology-%d"
remove_links_template = "../topology/remove/%s-remove-%d-links"
final_topology_base_template = "../topology/final/%s-final-topology-%d-power"
remove_links_base_template = "../topology/remove/%s-remove-%d-links-power"
solution_template = "%s-cplex-%0.1f.xml"
demand_file_template = "../demand/%s-%s/%0.1f/%d.txt"
result_file_template = "result-compare-%s-%0.1f"
middle_file_template = "middle-compare-%s-%0.1f"
solution_default = "global_opt_cplex_output.sol"
files = 1000

loop = 1

remove_links_n = {'abilene':5, 'geant':16, 'cernet2':4}

def dijkstra(g, length_graph, node_start):
    distances = {}
    Q = priorityDictionary()
    visited  = []

    for v in g:
        distances[v] = g.INFINITY
        Q[v] = g.INFINITY

    distances[node_start] = 0
    Q[node_start] = 0

    for v in Q:
        visited.append(v)
        if len(visited) == length_graph:
            break

        for u in g[v]:
            if u in visited:
                continue
            
            cost_vu = distances[v] + g[v][u]
            
            if cost_vu < distances[u]:
                distances[u] = cost_vu
                Q[u] = cost_vu
    return distances

for w in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
    for t in ['abilene', 'geant', 'cernet2']:
        connected_topology = connected_topology_template % t
        solution = solution_template % (t, w)
        result_file = result_file_template % (t, w)
        middle_file = middle_file_template % (t, w)


        global_routes = xml.get_route(solution)
        link_order = xml.get_link_order_with_attr(solution, connected_topology)
        path_len_routes = dict()
        path_len_routes_base = dict()
        path_len_shortest = dict()
        path_len_shortest_base = dict()
        for alpha in range(0, remove_links_n[t]):
            final_topology = final_topology_template % (t, alpha)
            remove_links = remove_links_template % (t, alpha)
            final_topology_base = final_topology_base_template % (t, alpha)
            remove_links_base = remove_links_base_template % (t, alpha)

            # Generate the global routes for traffic sets 
            # Calculate the global maximum utilization for specific traffic matrix sets

            global_routes_copy = deepcopy(global_routes)
            link_order_copy = deepcopy(link_order)
            new_global_routes = adjust.adjust_route(final_topology, remove_links, global_routes_copy, link_order_copy)
            #new_global_routes_fixed = adjust.fixed_route(new_global_routes)
            new_global_routes_fixed = new_global_routes

            global_routes_base_copy = deepcopy(global_routes)
            link_order_copy = deepcopy(link_order)
            new_global_routes_base = adjust.adjust_route(final_topology_base, remove_links_base, global_routes_base_copy, link_order_copy)
            #new_global_routes_base_fixed = adjust.fixed_route(new_global_routes_base)
            new_global_routes_base_fixed = new_global_routes_base

            for s,d in new_global_routes_fixed:
                route_paths = new_global_routes_fixed[s,d]
                path_len = 0
                for path, weight in route_paths:
                    path_len += (len(path) - 1) * weight
                path_len_routes[(alpha, s, d)] = path_len


            #print path_len_routes

            for s,d in new_global_routes_base_fixed:
                route_paths = new_global_routes_base_fixed[s,d]
                path_len = 0
                for path, weight in route_paths:
                    path_len += (len(path) - 1) * weight
                path_len_routes_base[(alpha, s, d)] = path_len

            g = DiGraph()
            f = open(final_topology) 
            line = f.readline()
            length_graph = int(line.rstrip().split(' ')[0])
            line = f.readline()
            while line:
                s = line.rstrip().split(' ')
                lls = int(s[0])
                lld = int(s[1])

                g.add_edge(lls, lld, 1);
                g.add_edge(lld, lls, 1);

                line = f.readline()
            f.close()

            for n in range(length_graph):
                distances = dijkstra(g, length_graph, n)
                
                for key in distances:
                    if key == n:
                        continue
                    path_len_shortest[(alpha, n, key)] = distances[key]

            g = DiGraph()
            f = open(final_topology_base) 
            line = f.readline()
            length_graph = int(line.rstrip().split(' ')[0])
            line = f.readline()
            while line:
                s = line.rstrip().split(' ')
                lls = int(s[0])
                lld = int(s[1])

                g.add_edge(lls, lld, 1);
                g.add_edge(lld, lls, 1);

                line = f.readline()
            f.close()

            for n in range(length_graph):
                distances = dijkstra(g, length_graph, n)
                
                for key in distances:
                    if key == n:
                        continue
                    path_len_shortest_base[(alpha, n, key)] = distances[key]
            #print path_len_shortest

        print t
        f = open('path_stretch_%s_%0.1f.txt' % (t, w), 'a')
        for alpha in range(0, remove_links_n[t]):
            max_stretching = 0
            sum_stretching = 0
            max_stretching_base = 0
            sum_stretching_base = 0
            num = 0
            base_s = 0
            base_d = 0
            for s in range(0, length_graph):
                for d in range(0, length_graph):
                    if s == d:
                        continue
                    
                    if path_len_routes_base[(alpha, s, d)] / path_len_shortest_base[(alpha, s, d)] < 1:
                        sum_stretching_base = sum_stretching_base + 1
                    else:
                        sum_stretching_base = sum_stretching_base + path_len_routes_base[(alpha, s, d)] / path_len_shortest_base[(alpha, s, d)]

                    if max_stretching_base < path_len_routes_base[(alpha, s, d)] / path_len_shortest_base[(alpha, s, d)]:
                        max_stretching_base = path_len_routes_base[(alpha, s, d)] / path_len_shortest_base[(alpha, s, d)]
                        base_s = s
                        base_d = d

                    if path_len_routes[(alpha, s, d)] / path_len_shortest[(alpha, s, d)] < 1:
                        sum_stretching = sum_stretching + 1
                    else:
                        sum_stretching = sum_stretching + path_len_routes[(alpha, s, d)] / path_len_shortest[(alpha, s, d)]

                    if max_stretching < path_len_routes[(alpha, s, d)] / path_len_shortest[(alpha, s, d)]:
                        max_stretching = path_len_routes[(alpha, s, d)] / path_len_shortest[(alpha, s, d)]

                    num = num + 1

            f.write('%d, %f, %f, %f, %f\n' % (alpha, max_stretching, sum_stretching/num, max_stretching_base, sum_stretching_base/num))
        f.close()

