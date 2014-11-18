from copy import deepcopy
import optimal_route_with_tm as optimal
import global_route_without_tm as common
import adjust_route_in_new_topology as adjust

# Generate performance 

connected_topology = "../topology/connected/geant-connected-topology"
final_topology = "../topology/final/geant-final-0-topology"
remove_links = "../topology/remove/geant-remove-0-links"
demand_file_template = "../demand/geant/%d.txt"
result_file = "result-geant-0"
begin = 36
files = 131

'''
connected_topology = "../topology/connected/abilene-connected-topology"
final_topology = "../topology/final/abilene-final-0-90-topology"
remove_links = "../topology/remove/abilene-remove-0-90-links"
demand_file_template = "../demand/abilene/XX02/%d.txt"
result_file = "result-abilene-0-90"
files = 288
'''

loop = 20
diff = 1000


# Generate the global routes for traffic sets 
# Calculate the global maximum utilization for specific traffic matrix sets
global_routes = common.global_routes(connected_topology)


for num in range(begin, files):
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
