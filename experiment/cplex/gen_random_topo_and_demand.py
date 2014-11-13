import random

def init_origin(topology, origin_file):
	# Node
	f = open(topology)
	node = (int)(f.readline().rstrip())
	f.close()
	
	# Bimodel

	random_num = 0
	left = [0, 1, 4]
	right = [2, 3, 5, 6]
	f = open(origin_file, 'w')
	f.write("%d\n" % node)
	'''
	while random_num < 4:
		s = random.randint(0, node-1)
		t = random.randint(0, node-1)

		if s != t:
			f.write("%d %d %0.6f\n" % (s, t, 0.45))
			random_num += 1
	'''
	cc = [([0] * node) for i in range(node)]
	for i in range(node):
		for j in range(node):
			if i != j:
				f.write("%d %d %0.6f\n" % (i, j, 1))

	f.close()
	

def generate_demand(origin_file, w, demand_file):
	f = open(origin_file)
	ff = open(demand_file, 'w')

	node = (int)(f.readline().rstrip())

	line = f.readline()
	while line:
		s = line.rstrip().split(" ")
		ff.write("%s %s %0.6f\n" % (s[0], s[1], \
				random.uniform(float(s[2]) / w, float(s[2]) * w)))
		line = f.readline()
	
	f.close()
	ff.close()

