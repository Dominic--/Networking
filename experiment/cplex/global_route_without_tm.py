import os
import paper_cplex_input_without_tm as cplex
import utilization_from_route as utils
import parse_xml as xml

def global_utilization(topology, routes, demand_file, loop):
    f = open(demand_file)
    node = (int)(f.readline().rstrip())
    line = f.readline()
    while line:
        s = line.rstrip().split(' ')
        s = [int(i) for i in s]
        for route in routes[s[0],s[1]]:
            route[1] = route[1] * (float)(s[2])
            line = f.readline()
    f.close()

    link_u_global_opt = utils.get_utilization(topology, routes, loop)
    print("Global Utilization is %f \n" % link_u_global_opt)

    return link_u_global_opt

def global_routes(topology):
    # Init
    remove_all_lp_or_sol_or_txt = "del *.lp *.sol *.txt >> log"
    remove_all_lp_or_sol = "del *.lp *.sol >> log"
    #os.system(remove_all_lp_or_sol_or_txt)

    # Get the upper bound of performance ratio for specific topology
    # Only be run once
    global_opt_cplex_input = "global_opt_cplex_input.lp"
    global_opt_cplex_output = "global_opt_cplex_output.sol"
    cplex.generate_cplex_lp_file(topology, global_opt_cplex_input)

    global_opt_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
            (global_opt_cplex_input, global_opt_cplex_output)	
    #os.system(global_opt_cplex_cmd)

    global_opt_upper_bound = xml.get_object(global_opt_cplex_output)
    print("Upper Bound is %f" % global_opt_upper_bound)

    global_opt_routes = xml.get_route(global_opt_cplex_output)
    #print(global_opt_routes)

    return global_opt_routes
