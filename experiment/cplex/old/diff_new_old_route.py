import random
import os
import parseXML as xml
import new_best as best
from dfs import *

#topology = "weights.intra.new"
base = "geantTopo"
demand_file = "demand.txt"
gravities = [5*i for i in range(11, 25)]
loop = 20
out = True

for gravity in gravities:
	topology = '%s%d' % (base, gravity)

	remove_all_lp_or_sol_or_txt = "del *.lp *.sol *.txt >> log"
	remove_all_lp_or_sol = "del *.lp *.sol >> log"
	os.system(remove_all_lp_or_sol_or_txt)

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
	min_cplex_input = "min_cplex_input.lp"
	min_cplex_output = "min_cplex_output.sol"
	best.min_route(topology, demand_file, min_cplex_input, gravity)

	min_cplex_cmd = 'cplex -c "read %s" "optimize" "write %s" >> log' % \
		(min_cplex_input, min_cplex_output)	
	os.system(min_cplex_cmd)

	min_routes = xml.get_f(min_cplex_output, demand_file)
	link_u_min = xml.get_object(min_cplex_output)

	#print(link_u_min)
	#print(min_routes)
	#print(min_routes[(0,1)])

	print('-------begin dfs-----------')

	st_paths = {}
	for key in min_routes.keys():
		value = min_routes[key]
		#print(key)
		g = Graph()
		s,t = key
		g.add_node(s)
		g.add_node(t)
		for v in value:
			g.add_node(v[0])
			g.add_node(v[1])
			g.add_edge((v[0], v[1], v[2]))
		st_paths[key] = g.find_path(s, t)

	#print(st_paths)
	print('----------begin random path------------')

	min_dd = [([0] * node) for i in range(node)]
	min_loop = 10000

	for l in range(loop):
		st_path = {}
		for key in st_paths.keys():
			value = st_paths[key]
			random_sum = 0
			for v in value:
				random_sum += v[1]
			random_num = random.uniform(0, random_sum)
			for v in value:
				if random_num < v[1]:
					st_path[key] = [v[0], random_sum]
				else:
					random_num -= v[1]

		#print(st_path)
		dd = [([0] * node) for i in range(node)]

		for key in st_path.keys():
			v = st_path[key]
			path = v[0]
			weight = v[1]
			for i in range(len(path) - 1):
				dd[path[i]][path[i+1]] += weight
				dd[path[i+1]][path[i]] += weight

		link_u = 0
		for i in range(node):
			for j in range(node):
				if cm[i][j] != 0 and dd[i][j] / cm[i][j] > link_u:
					link_u = dd[i][j] / cm[i][j]

		if link_u < min_loop:
			min_loop = link_u
			for i in range(node):
				for j in range(node):
					min_dd[i][j] = dd[i][j]

		print('gravity: %f, new utilization for %d: %f\n' % (gravity, l, link_u))

	if out:
		fd = open('%s-%0.1f' % (topology, gravity), 'w')
		fd.write('%d\n%d\n%0.6f\n' % (node, links, min_loop))
		for i in range(node):
			for j in range(node):
				if cm[i][j] != 0 and i < j:
					fd.write('%d %d %0.6f %0.6f\n' % (i, j, min_dd[i][j], min_dd[i][j]/cm[i][j]))
		fd.close()

	print('gravity: %f, old utilization: %f\n' % (gravity, link_u_min))

