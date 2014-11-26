from copy import deepcopy
import optimal_route_with_tm as optimal
import global_route_with_tm_bound as common
import adjust_route_in_new_topology as adjust

# Generate performance 

is_gravity = True
type_random = "bimodal"

connected_topology_template = "../topology/connected/%s-connected-topology"
final_topology_template = "../topology/final/%s-final-topology-%d"
remove_links_template = "../topology/remove/%s-remove-%d-links"
final_topology_base_template = "../topology/final/%s-final-topology-%d-base"
remove_links_base_template = "../topology/remove/%s-remove-%d-links-base"
demand_file_template = "../demand/%s-%s/%d.txt"
result_file_template = "result-compare-%s"
files = 100

loop = 20
diff = 1000

for t in ['abilene', 'geant']:
    result_file = result_file_template % (t)
    for alpha in range(1, 5):
        connected_topology = connected_topology_template % t
        final_topology = final_topology_template % (t, alpha)
        remove_links = remove_links_template % (t, alpha)
        final_topology_base = final_topology_base_template % (t, alpha)
        remove_links_base = remove_links_base_template % (t, alpha)

        upper = 0
        if is_gravity:
            upper = 1.5
            type_random = "gravity"
        else:
            if t == 'abilene':
                upper = 9424.0
            elif t == 'geant':
                upper = 1956.0

        bound = [0, 1.5]

        # Generate the global routes for traffic sets 
        # Calculate the global maximum utilization for specific traffic matrix sets
        global_routes = common.global_routes(connected_topology, bound, is_gravity)

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
            #print('Optimal Utilization is %f\n' % optimal_utilization)
            #f.write('%10.4f\t' % optimal_utilization)

            #TODO Change Route
            #print("Begin adjust route")
            global_routes_copy = deepcopy(global_routes)
            new_global_routes = adjust.adjust_route(final_topology, remove_links, global_routes_copy)

            #print("Begin calculate utilization")
            global_utilization = common.global_utilization(final_topology, new_global_routes, demand_file, loop)
            #print('Global Utilization is %f\n' % global_utilization)
            #f.write('%10.4f\t' % global_utilization)

            global_routes_base_copy = deepcopy(global_routes)
            new_global_routes_base = adjust.adjust_route(final_topology_base, remove_links_base, global_routes_base_copy)
            global_utilization_base = common.global_utilization(final_topology_base, new_global_routes_base, demand_file, loop)

            if max_utilization_base < (global_utilization_base / optimal_utilization):
                max_utilization_base = global_utilization_base / optimal_utilization
            
            if max_utilization < (global_utilization / optimal_utilization):
                max_utilization = global_utilization / optimal_utilization
        
        f = open(result_file, 'a')
        print("Remove %d links -- Base : %.4f New : %.4f\n" % (alpha, max_utilization_base, max_utilization))
        f.write("Remove %d links -- Base : %.4f New : %.4f\n" % (alpha, max_utilization_base, max_utilization))
        f.close()

