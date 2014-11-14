import os
import parse_xml as xml
import paper_cplex_input_without_tm as opt_no_w
#import now as opt_with_w
#import generate as gen
import utilization as util
import min_cplex_input_with_tm as best

topology = "../topology/final/abilene-final-topology"

# Init
remove_all_lp_or_sol_or_txt = "del *.lp *.sol *.txt >> log"
remove_all_lp_or_sol = "del *.lp *.sol >> log"
os.system(remove_all_lp_or_sol_or_txt)


# Get the upper bound of performance ratio for specific topology
# Only be run once
global_opt_cplex_input = "global_opt_cplex_input.lp"
global_opt_cplex_output = "global_opt_cplex_output.sol"
opt_no_w.global_opt(topology, global_opt_cplex_input)

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


'''
p_w = dict()
o_w = dict()
for i in range(2, 11):
	p_w[i/2] = 0
	o_w[i/2] = 0


for o in range(1):
	origin_file = "origin.txt"
	gen.init_origin(topology, origin_file)
	
	for itr in range(5):
		print('--------------------%d------------------------' % itr)
		for w in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:
			os.system(remove_all_lp_or_sol)

			# OPT
			opt_cplex_input = "opt_cplex_input.lp"
			opt_cplex_output = "opt_cplex_output.sol"
			opt_with_w.opt(topology, origin_file, w, opt_cplex_input)

			opt_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
					(opt_cplex_input, opt_cplex_output)
			os.system(opt_cplex_cmd)

			opt_routes = xml.get_variables(opt_cplex_output)

			# Generate demand with w
			demand_file = "demand.txt"
			gen.generate_demand(origin_file, w, demand_file)


			# Calculate link utilizaiton of the routes(by global_opt) for specific topology
			link_u_global_opt = util.get_link_utilization(topology, demand_file, global_opt_routes)
			link_u_opt = util.get_link_utilization(topology, demand_file, opt_routes)


			# Get lowest link utilizaiton among all posible routes
			min_cplex_input = "min_cplex_input.lp"
			min_cplex_output = "min_cplex_output.sol"
			best.min_route(topology, demand_file, min_cplex_input)

			min_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
				(min_cplex_input, min_cplex_output)	
			os.system(min_cplex_cmd)

			min_routes = xml.get_variables(min_cplex_output)
			link_u_min = xml.get_object(min_cplex_output)
			#for g in global_opt_routes:
			#	print(g, global_opt_routes[g] - min_routes[g])


			# Calculate link utilizaiton of the min route for specific topology
			#link_u_min = util.get_link_utilization(topology, demand_file, min_routes)


			# Get Performance Ratio
			p_ratio = link_u_global_opt / link_u_min
			
			if p_w[w] < p_ratio:
				p_w[w] = p_ratio

			o_ratio = link_u_opt / link_u_min
			
			if o_w[w] < o_ratio:
				o_w[w] = o_ratio


	print("----------------------------pw------------------------------")
	for i in range(2, 11):
		print(p_w[i/2])

	print("----------------------------ow------------------------------")
	for i in range(2, 11):
		print(o_w[i/2])

'''
