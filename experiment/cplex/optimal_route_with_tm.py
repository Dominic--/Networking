import random, os
import parse_xml as xml
import min_cplex_input_with_tm as cplex
import utilizaiton_from_route as utils
from dfs import *


topology = '../topology/final/abilene-final-topology'
demand_file = "demand.txt"
loop = 20

def optimal_utilization(topology, demand_file):
    # init cm and dd
    f = open(topology)
    node = (int)(f.readline().rstrip())
    links = (int)(f.readline().rstrip())
    cm = [([0] * node) for i in range(node)]

    line = f.readline()
    while line:
        s = line.rstrip().split(' ')
        cm[int(s[0])][int(s[1])] = float(s[3])
        cm[int(s[1])][int(s[0])] = float(s[3])
        line = f.readline()
    f.close()

    # Get lowest link utilizaiton among all posible routes
    remove_all_lp_or_sol_or_txt = "del *.lp *.sol *.txt >> log"
    remove_all_lp_or_sol = "del *.lp *.sol >> log"
    os.system(remove_all_lp_or_sol_or_txt)

    min_cplex_input = "min_cplex_input.lp"
    min_cplex_output = "min_cplex_output.sol"
    cplex.min_route(topology, demand_file, min_cplex_input)

    min_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
        (min_cplex_input, min_cplex_output)	
    os.system(min_cplex_cmd)

    min_routes = xml.get_f(min_cplex_output, demand_file)
    link_u_min = xml.get_object(min_cplex_output)

    print("Old Utilization is %f \n" % link_u_min)

    link_u = utils.get_utilization(topology, min_routes, loop)

    print('New Utilization is %f \n' % link_u)

    return link_u
