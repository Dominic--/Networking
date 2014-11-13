import xml.dom.minidom

def get_link_utilization(topology, demand, variable):
	f = open(topology)
	
	node = (int)(f.readline().rstrip())
	cm = [([0] * node) for i in range(node)]

	link = list()
	line = f.readline()
	while line:
		s = line.rstrip().split(" ")
		cm[int(s[0])][int(s[1])] = 1 / (float)(s[2])
		cm[int(s[1])][int(s[0])] = 1 / (float)(s[2])
		link.append([int(s[0]), int(s[1])])
		line = f.readline()
	f.close()


	d = [([0] * node) for i in range(node)]
	f = open(demand)
	line = f.readline()
	while line:
		s = line.rstrip().split(" ")
		d[int(s[0])][int(s[1])] = (float)(s[2])
		line = f.readline()
	f.close()


	ll = len(link)
	result = 0
	for l in range(ll):
		tmp  = 0
		for j in range(node):
			for k in range(node):
				if j == k:
					continue
				
				route = "f%da%da%da%d" % (link[l][0], link[l][1], j, k)
				route_r = "f%da%da%da%d" % (link[l][1], link[l][0], j, k)
				if route in variable:
					tmp += variable[route] * d[j][k]

				if route_r in variable:
					tmp += variable[route_r] * d[j][k]
		tmp = tmp / cm[link[l][0]][link[l][1]]
		if tmp > result:
			result = tmp


	return result
