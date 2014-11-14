def generate_cplex_lp_file(topology, output):
	f = open(topology)

	# Node
	node = (int)(f.readline().rstrip().split(" ")[0])

	# Capacity Matrix
	# Link Set
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
	ll = len(link)

	# Begin
	f = open(output, 'w')
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


	# cap(m)pai(l,m) <= r
	for i in range(ll):
		line = ""
		for j in range(ll):
			if j != 0:
				line += "+ "
			line += "%0.6fpai%da%d " % (cm[link[j][0]][link[j][1]], i, j)
		line += " - r <= 0\n"
		f.write(line)
		#break


	# fij(l)/cap(l) = pl(i,j)
	for i in range(ll):
		for j in range(node):
			for k in range(node):
				if j == k:
					continue
				line = "%0.6ff%da%da%da%d + %0.6ff%da%da%da%d  " % \
						(1/cm[link[i][0]][link[i][1]], link[i][0], link[i][1], j, k,\
						1/cm[link[i][0]][link[i][1]], link[i][1], link[i][0], j, k)
				if j == k:
					line += " = 0\n"
				else:
					line += " - p%da%da%d <= 0\n" % (i, j, k)
				f.write(line)
				#break
			#break
		#break


	# pai(l, link-of(e)) + pl(i,j) - pl(i, k) >= 0
	for i in range(ll):
		for j in range(node):
			for k in range(ll):
				line = "pai%da%d + p%da%da%d - p%da%da%d >= 0\n" % \
						(i, k, i, j, link[k][0], i, j, link[k][1])
				line += "pai%da%d + p%da%da%d - p%da%da%d >= 0\n" % \
						(i, k, i, j, link[k][1], i, j, link[k][0])
				f.write(line)
				#break
			#break
		#break


	# bounds
	f.write("bound\n")
	for i in range(ll):
		for j in range(ll):
			f.write("0 <= pai%da%d\n" % (i, j))

	for i in range(ll):
		for j in range(node):
			for k in range(node):
				if j != k:
					f.write("0 <= p%da%da%d\n" % (i, j, k))
					f.write("0 <= f%da%da%da%d <= 1\n" % (link[i][0], link[i][1], j, k))
					f.write("0 <= f%da%da%da%d <= 1\n" % (link[i][1], link[i][0], j, k))
				else:
					f.write("0 <= p%da%da%d <= 0\n" % (i, j, k))

	# End
	f.write("end\n")
	f.close()

