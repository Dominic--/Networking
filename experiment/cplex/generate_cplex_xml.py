import parse_xml as xml
import os
import global_route_with_tm_bound as common

# Generate performance 

is_gravity = True
type_random = "bimodal"

connected_topology_template = "../topology/connected/%s-connected-topology"
solution_template = "%s-cplex-%0.1f.xml"
solution_default = "global_opt_cplex_output.sol"


for t in ['cernet2','abilene', 'geant']:
    for w in [1.5, 2, 2.5, 3, 3.5, 4]:
        connected_topology = connected_topology_template % t

        common.generate_sol(connected_topology, [0, w], is_gravity)
        print xml.get_object(solution_default)

        solution = solution_template % (t, w)
        #print solution
        os.system("mv %s %s" % (solution_default, solution))
