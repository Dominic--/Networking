import random

def min_route(topology, demand_file, outfile, gravity):
	f = open(topology)

	# Node
	node = (int)(f.readline().rstrip())
	links = (int)(f.readline().rstrip())
	print(node)
	print(links)

	# Capacity Matrix
	# Link Set
	cm = [([0] * node) for i in range(node)]
	link = list()
	line = f.readline()
	while line:
		s = line.rstrip().split(" ")
		cm[int(s[0])][int(s[1])] = (float)(s[3])
		cm[int(s[1])][int(s[0])] = (float)(s[3])
		link.append([int(s[0]), int(s[1])])
		line = f.readline()
	f.close()
	ll = len(link)

	f = open(demand_file, 'w')
	f.write('%d\n' % node)
	d = [([0] * node) for i in range(node)]
	for i in range(node):
		for j in range(node):
			if i == j:
				continue
			combined_s = 0
			combined_t = 0
			for k in range(node):
				combined_s += cm[i][k]
			for k in range(node):
				combined_t += cm[j][k]
			d[i][j] = combined_s * combined_t * gravity / 50000000
			f.write('%d %d %f\n' % (i, j, d[i][j]))
	f.close()

	# Begin
	f = open(outfile, 'w')
	f.write("Min\nr\nsubject to\n")


	# Generate CPLEX
	# f(l1, l2, s, t) is routing
	for i in range(node):
		for j in range(node):
			if i == j:
				continue
			for k in range(node):
				line = ""
				first = True
				for l in range(ll):
					# l, k is the tail
					if k == link[l][1]:
						if not first:
							line += "+ f%da%da%da%d " % (link[l][0], link[l][1], i, j)
						else:
							line += "f%da%da%da%d " % (link[l][0], link[l][1], i, j)
							first = False

					# l, k is the head
					if k == link[l][0]:
						if not first:
							line += "- f%da%da%da%d " % (link[l][0], link[l][1], i, j)
						else:
							line += "-f%da%da%da%d " % (link[l][0], link[l][1], i, j)
							first = False
						
					# -l, k is the tail
					if k == link[l][0]:
						if not first:
							line += "+ f%da%da%da%d " % (link[l][1], link[l][0], i, j)
						else:
							line += "f%da%da%da%d " % (link[l][1], link[l][0], i, j)
							first = False
		
					# -l, k is the head
					if k == link[l][1]:
						if not first:
							line += "- f%da%da%da%d " % (link[l][1], link[l][0], i, j)
						else:
							line += "-f%da%da%da%d " % (link[l][1], link[l][0], i, j)
							first = False
				
				if k == j:
					line += "= 1\n"
				elif k == i:
					line += "= -1\n"
				else:
					line += "= 0\n"
				f.write(line)

	for l in range(ll):
		line = ""
		first = True
		for j in range(node):
			for k in range(node):
				if j == k:
					continue
				if not first:
					line += "+ "
				line += "%0.6ff%da%da%da%d " % \
						(d[j][k], link[l][0], link[l][1], j, k)
				first = False
				if not first:
					line += "+ "
				line += "%0.6ff%da%da%da%d " % \
						(d[j][k], link[l][1], link[l][0], j, k)
				first = False
		line += "- %0.6fr <= 0\n" % cm[link[l][0]][link[l][1]]
		f.write(line)
					
	# bounds
	f.write("bound\n")
	for i in range(ll):
		for j in range(node):
			for k in range(node):
				if j != k:
					f.write("0 <= f%da%da%da%d <= 1\n" % (link[i][0], link[i][1], j, k))
					f.write("0 <= f%da%da%da%d <= 1\n" % (link[i][1], link[i][0], j, k))

	# End
	f.write("end\n")
	f.close()


