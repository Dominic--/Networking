import random, os
import min_cplex_input_with_tm as cplex
import utilization_from_route as utils
import parse_xml as xml

def optimal_utilization(topology, demand_file, loop):

    # Get lowest link utilizaiton among all posible routes
    remove_all_lp_or_sol_or_txt = "del *.lp *.sol *.txt >> log"
    remove_all_lp_or_sol = "del *.lp *.sol >> log"
    os.system(remove_all_lp_or_sol_or_txt)

    min_cplex_input = "min_cplex_input.lp"
    min_cplex_output = "min_cplex_output.sol"
    cplex.generate_cplex_lp_file(topology, demand_file, min_cplex_input)

    min_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
        (min_cplex_input, min_cplex_output)	
    os.system(min_cplex_cmd)

    #link_u_min = xml.get_object(min_cplex_output)
    #print("Old Utilization is %f \n" % link_u_min)

    min_routes = xml.get_route_with_demand(min_cplex_output, demand_file)
    link_u = utils.get_utilization(topology, min_routes, loop)
    #print('Optimal Utilization is %f' % link_u)

    return link_u
