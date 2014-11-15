import optimal_route_with_tm as optimal
import global_route_without_tm as common
import adjust_route_in_new_topology as adjust

# Generate performance 

demand_file = "../demand/abilene.txt"

connected_topology = "../topology/connected/abilene-connected-topology"
final_topology = "../topology/final/abilene-final-0-topology"
remove_links = "../topology/remove/abilene-remove-0-links"

loop = 20

# Calculate the optimal maximum utilization for specific traffic matrix
optimal_utilization = optimal.optimal_utilization(connected_topology, demand_file, loop)

# Generate the global routes for traffic sets 
# Calculate the global maximum utilization for specific traffic matrix 
global_routes = common.global_routes(final_topology)

#TODO Change Route
print("Begin adjust route")
new_global_routes = adjust.adjust_route(remove_links, global_routes)

print("Begin calculate utilization")
global_utilization = common.global_utilization(final_topology, new_global_routes, demand_file)

print("Diff is %f \n" % global_utilization / optimal_utilization)
