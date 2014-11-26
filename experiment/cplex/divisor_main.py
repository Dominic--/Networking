from copy import deepcopy
import optimal_route_with_tm as optimal
import global_route_without_tm as common
import adjust_route_in_new_topology as adjust

# Generate performance 
'''
connected_topology_template = "../topology/connected/geant-connected-topology"
final_topology_template = "../topology/final/geant-final-1-%s-topology-power"
remove_links_templae = "../topology/remove/geant-remove-1-%s-links-power"
demand_file_template = "../demand/real-geant/%d.txt"
result_file_template = "result-geant-1-%s-power"
begin = 36
files = 131
'''
connected_topology = "../topology/connected/abilene-connected-topology"
final_topology_template = "../topology/final/abilene-final-topology-%d"
remove_links_templae = "../topology/remove/abilene-remove-%d-links"
final_topology_base_template = "../topology/final/abilene-final-%d-topology-base"
remove_links_base_template = "../topology/remove/abilene-remove-%d-links-base"
demand_file_template = "../demand/real-abilene/XX02/%d.txt"
result_file = "result-abilene-1-90-power"
loop = 20
begin = 0
files = 288

global_routes = common.global_routes(connected_topology)
max_utl = 0
for num in range(begin, files):
    demand_file = demand_file_template % num
    f = open(demand_file, "r")
    line = f.readline()
    f.close()
    if int(line.strip()) == 0:
        continue
    
    '''
    f = open(result_file,"a")
    # Calculate the optimal maximum utilization for specific traffic matrix
    optimal_utilization = optimal.optimal_utilization(connected_topology, demand_file, loop)
    print('Optimal Utilization is %f\n' % optimal_utilization)
    f.write('%10.4f\t' % optimal_utilization)
    '''
    #print("Begin adjust route")
    global_routes_copy = deepcopy(global_routes)
    new_global_routes = adjust.adjust_route(final_topology, remove_links, global_routes_copy)

    #print("Begin calculate utilization")
    global_utilization = common.global_utilization(final_topology, new_global_routes, demand_file, loop)
    #print('Global Utilization is %f\n' % global_utilization)
    
    if global_utilization > max_utl:
        max_utl = global_utilization

print max_utl
'''
    if diff > global_utilization / optimal_utilization:
        diff = global_utilization / optimal_utilization
    print("Now Diff is %f" % (global_utilization / optimal_utilization))
    print("Diff is %f" % diff)
    f.write("%6.4f\t" % (global_utilization / optimal_utilization))
    f.write("%6.4f\n" % diff)

    f.close()
'''
'''
for alpha in ['80', '85', '90', '95', '100']:

    connected_topology = connected_topology_template % alpha
    final_topology = final_topology_template % alpha
    remove_links = remove_links_templae % alpha
    result_file = result_file_template % alpha

    loop = 20
    diff = 1000


    # Generate the global routes for traffic sets 
    # Calculate the global maximum utilization for specific traffic matrix sets
    global_routes = common.global_routes(connected_topology)


    for num in range(files):
        print("Round %d\n" % num)

        demand_file = demand_file_template % num
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
'''
