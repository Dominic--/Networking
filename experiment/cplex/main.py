import optimal_route_with_tm as optimal
import global_route_without_tm as common
import adjust_route_in_new_topology as adjust

# Generate performance 

connected_topology = "../topology/connected/geant-connected-topology"
final_topology = "../topology/final/geant-final-1-topology"
remove_links = "../topology/remove/geant-remove-1-links"
loop = 20

diff = 1000

# Generate the global routes for traffic sets 
# Calculate the global maximum utilization for specific traffic matrix sets
global_routes = common.global_routes(connected_topology)


for num in range(11460):
    print("Round %d\n" % num)

    demand_file = "../demand/geant/%d.txt" % num
    f = open(demand_file, "r")
    line = f.readline()
    f.close()
    if int(line.strip()) == 0:
        continue

    f = open("result-geant","a")
    # Calculate the optimal maximum utilization for specific traffic matrix
    optimal_utilization = optimal.optimal_utilization(final_topology, demand_file, loop)
    print('Optimal Utilization is %f\n' % optimal_utilization)
    f.write('Optimal Utilization is %f\n' % optimal_utilization)

    #TODO Change Route
    print("Begin adjust route")
    new_global_routes = adjust.adjust_route(final_topology, remove_links, global_routes)

    print("Begin calculate utilization")
    global_utilization = common.global_utilization(final_topology, global_routes, demand_file, loop)

    if diff > global_utilization / optimal_utilization:
        diff = global_utilization / optimal_utilization
    print("Now Diff is %f" % (global_utilization / optimal_utilization))
    f.write("Now Diff is %f" % (global_utilization / optimal_utilization))
    print("Diff is %f" % diff)
    f.write("Diff is %f" % diff)

    f.close()
