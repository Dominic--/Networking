import os
import parse_xml as xml
import paper_cplex_input_without_tm as cplex
#import now as opt_with_w
#import generate as gen
import utilization_from_route as utils

topology = "../topology/final/abilene-final-topology"
demand_file = 'demand.txt'
loop = 20

def global_utilization(topology, demand_file):
    # Init
    remove_all_lp_or_sol_or_txt = "del *.lp *.sol *.txt >> log"
    remove_all_lp_or_sol = "del *.lp *.sol >> log"
    os.system(remove_all_lp_or_sol_or_txt)

    # Get the upper bound of performance ratio for specific topology
    # Only be run once
    global_opt_cplex_input = "global_opt_cplex_input.lp"
    global_opt_cplex_output = "global_opt_cplex_output.sol"
    cplex.global_opt(topology, global_opt_cplex_input)

    global_opt_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
            (global_opt_cplex_input, global_opt_cplex_output)	
    os.system(global_opt_cplex_cmd)

    global_opt_upper_bound = xml.get_object(global_opt_cplex_output)
    global_opt_routes = xml.get_variables(global_opt_cplex_output)
    link_u_global_opt = util.get_link_utilization(topology, demand_file, global_opt_routes)

    print(global_opt_upper_bound)
    print(link_u_global_opt)

    # Get the min route for the specific topology
    min_cplex_input = "min_cplex_input.lp"
    min_cplex_output = "min_cplex_output.sol"
    best.min_route(topology, demand_file, min_cplex_input)

    min_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
        (min_cplex_input, min_cplex_output)	
    os.system(min_cplex_cmd)

    min_routes = xml.get_variables(min_cplex_output)
    link_u_min = xml.get_object(min_cplex_output)

    print(link_u_min)

    return link_u_min

