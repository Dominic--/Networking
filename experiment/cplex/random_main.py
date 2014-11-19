from copy import deepcopy
import optimal_route_with_tm as optimal
import global_route_with_tm_bound as common
import adjust_route_in_new_topology as adjust

# Generate performance 

is_gravity = False

connected_topology_template = "../topology/connected/%s-connected-topology"
final_topology_template = "../topology/final/%s-final-0-%s-topology"
remove_links_template = "../topology/remove/%s-remove-0-%s-links"
demand_file_template = "../demand/%s-geant/%d.txt"
result_file_template = "result-%s-0-%s"
files = 1000

loop = 20
diff = 1000

for t in ['abilene', 'geant']:
    for alpha in ['80', '85', '90', '95', '100']:
        connected_topology = connected_topology_template % t
        final_topology = final_topology_template % (t, alpha)
        remove_links = remove_links_template % (t, alpha)
        result_file = result_file_template % (t, alpha)

        upper = 0
        if is_gravity:
            upper = 0.001
        else:
            if t == 'abilene':
                upper = 9424.0
            elif t == 'geant':
                upper = 1956.0

        bound = [0, upper]

        # Generate the global routes for traffic sets 
        # Calculate the global maximum utilization for specific traffic matrix sets
        global_routes = common.global_routes(connected_topology, bound, is_gravity)

        for num in range(files):
            print("Round %d\n" % num)

            demand_file = demand_file_template % (t, num)
            f = open(demand_file, "r")
            line = f.readline()
            f.close()
            if int(line.strip()) == 0:
                continue

            f = open(result_file,"a")
            # Calculate the optimal maximum utilization for specific traffic matrix
            optimal_utilization = optimal.optimal_utilization(connected_topology, demand_file, loop)
            print('Optimal Utilization is %f\n' % optimal_utilization)
            f.write('%10.4f\t' % optimal_utilization)

            #TODO Change Route
            print("Begin adjust route")
            global_routes_copy = deepcopy(global_routes)
            new_global_routes = adjust.adjust_route(final_topology, remove_links, global_routes_copy)

            print("Begin calculate utilization")
            global_utilization = common.global_utilization(final_topology, new_global_routes, demand_file, loop)
            print('Global Utilization is %f\n' % global_utilization)
            f.write('%10.4f\t' % global_utilization)

            if diff > global_utilization / optimal_utilization:
                diff = global_utilization / optimal_utilization
            print("Now Diff is %f" % (global_utilization / optimal_utilization))
            print("Diff is %f" % diff)
            f.write("%6.4f\t" % (global_utilization / optimal_utilization))
            f.write("%6.4f\n" % diff)

            f.close()
