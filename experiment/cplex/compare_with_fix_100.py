from copy import deepcopy
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
final_topology_base_template = "../topology/final/%s-final-topology-%d-base"
remove_links_base_template = "../topology/remove/%s-remove-%d-links-base"
solution_template = "%s-connected-cplex.xml"
demand_file_template = "../demand/%s-%s/%d.txt"
result_file_template = "result-compare-fix-%s"
solution_default = "global_opt_cplex_output.sol"
files = 100
fix_num = 100

loop = 1

remove_links_n = {'abilene':2, 'geant':5}

for t in ['abilene', 'geant']:
    connected_topology = connected_topology_template % t
    solution = solution_template % t
    #solution = solution_default
    result_file = result_file_template % (t)

    #common.generate_sol(connected_topology, [0, 1.5], is_gravity)
    print xml.get_object(solution)
    global_routes = xml.get_route(solution)
    link_order = xml.get_link_order_with_attr(solution, connected_topology)
    for alpha in range(remove_links_n[t], remove_links_n[t] + 1):
        final_topology = final_topology_template % (t, alpha)
        remove_links = remove_links_template % (t, alpha)
        final_topology_base = final_topology_base_template % (t, alpha)
        remove_links_base = remove_links_base_template % (t, alpha)

        # Generate the global routes for traffic sets 
        # Calculate the global maximum utilization for specific traffic matrix sets

        global_routes_copy = deepcopy(global_routes)
        link_order_copy = deepcopy(link_order)
        new_global_routes = adjust.adjust_route(final_topology, remove_links, global_routes_copy, link_order_copy)

        global_routes_base_copy = deepcopy(global_routes)
        link_order_copy = deepcopy(link_order)
        new_global_routes_base = adjust.adjust_route(final_topology_base, remove_links_base, global_routes_base_copy, link_order_copy)

        for fn in range(fix_num):
            new_global_routes_copy = deepcopy(new_global_routes)
            new_global_routes_base_copy = deepcopy(new_global_routes_base)
            new_global_routes_fixed = adjust.fixed_route(new_global_routes)
            new_global_routes_base_fixed = adjust.fixed_route(new_global_routes_base)

            max_utilization = 0
            max_utilization_base = 0
            for num in range(files):
                print("Round %d\n" % num)

                demand_file = demand_file_template % (type_random, t, num)
                f = open(demand_file, "r")
                line = f.readline()
                f.close()
                if int(line.strip()) == 0:
                    continue

                #f = open(result_file,"a")
                # Calculate the optimal maximum utilization for specific traffic matrix
                optimal_utilization = optimal.optimal_utilization(connected_topology, demand_file, loop)
                print optimal_utilization
                #print('Optimal Utilization is %f\n' % optimal_utilization)
                #f.write('%10.4f\t' % optimal_utilization)

                #TODO Change Route
                #print("Begin adjust route")
                #global_routes_copy = deepcopy(global_routes)
                #link_order_copy = deepcopy(link_order)
                #new_global_routes = adjust.adjust_route(final_topology, remove_links, global_routes_copy, link_order_copy)

                #print("Begin calculate utilization")
                new_global_routes_fixed_copy = deepcopy(new_global_routes_fixed)
                global_utilization = common.global_utilization(final_topology, new_global_routes_fixed_copy, demand_file, 1)
                print global_utilization / optimal_utilization
                #print('Global Utilization is %f\n' % global_utilization)
                #f.write('%10.4f\t' % global_utilization)

                #global_routes_base_copy = deepcopy(global_routes)
                #link_order_copy = deepcopy(link_order)
                #new_global_routes_base = adjust.adjust_route(final_topology_base, remove_links_base, global_routes_base_copy, link_order_copy)
                new_global_routes_base_fixed_copy = deepcopy(new_global_routes_base_fixed)
                global_utilization_base = common.global_utilization(final_topology_base, new_global_routes_base_fixed_copy, demand_file, 1)
                print global_utilization_base / optimal_utilization

                if max_utilization_base < (global_utilization_base / optimal_utilization):
                    max_utilization_base = global_utilization_base / optimal_utilization
                
                if max_utilization < (global_utilization / optimal_utilization):
                    max_utilization = global_utilization / optimal_utilization
            
            f = open(result_file, 'a')
            print("Fix %d Remove %d links -- Base : %.4f New : %.4f\n" % (fn, alpha, max_utilization_base, max_utilization))
            f.write("Fix %d Remove %d links -- Base : %.4f New : %.4f\n" % (fn, alpha, max_utilization_base, max_utilization))
            f.close()


