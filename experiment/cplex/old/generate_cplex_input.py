# New Topology File Name
topology = "weights.intra.new"
#topology = "simple.intra.new"
w = 5

f = open(topology)

# Node
node = (int)(f.readline().rstrip())

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

# sum(bij*supl(i,j) - aij*slowl(i,j) <= 0)
a = [([0] * node) for i in range(node)]
b = [([0] * node) for i in range(node)]

d = [([0] * node) for i in range(node)]
d[0][4] = 0.6
d[5][3] = 0.4
d[2][6] = 0.3
d[1][6] = 0.1
d[3][1] = 0.1
d[3][6] = 0.15
# init a,b  with w, d
for i in range(node):
	for j in range(node):
		a[i][j] = d[i][j] / w
		b[i][j] = d[i][j] * w

#print(cm[0][0])
#print(len(link))

# Begin
f = open("cplex.lp", 'w')
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
						line += "+ %0.6ff%da%da%da%d " % (d[i][j], link[l][0], link[l][1], i, j)
					else:
						line += "%0.6ff%da%da%da%d " % (d[i][j], link[l][0], link[l][1], i, j)
						first = False

				# l, k is the head
				if k == link[l][0]:
					if not first:
						line += "- %0.6ff%da%da%da%d " % (d[i][j], link[l][0], link[l][1], i, j)
					else:
						line += "-%0.6ff%da%da%da%d " % (d[i][j], link[l][0], link[l][1], i, j)
						first = False
					
				# -l, k is the tail
				if k == link[l][0]:
					if not first:
						line += "+ %0.6ff%da%da%da%d " % (d[i][j], link[l][1], link[l][0], i, j)
					else:
						line += "%0.6ff%da%da%da%d " % (d[i][j], link[l][1], link[l][0], i, j)
						first = False
	
				# -l, k is the head
				if k == link[l][1]:
					if not first:
						line += "- %0.6ff%da%da%da%d " % (d[i][j], link[l][1], link[l][0], i, j)
					else:
						line += "-%0.6ff%da%da%da%d " % (d[i][j], link[l][1], link[l][0], i, j)
						first = False
			
			if k == j:
				line += "= %0.6f\n" % (d[i][j])
			elif k == i:
				line += "= %0.6f\n" % (-d[i][j])
			else:
				line += "= 0\n"
			f.write(line)


for l in range(ll):
	line = ""
	line_r = ""
	first = True
	for j in range(node):
		for k in range(node):
			if j == k:
				continue
			if not first:
				line += "+ "
				line_r += "+ "
			line += "%0.6ff%da%da%da%d " % \
					(d[j][k], link[l][0], link[l][1], j, k)
			line_r += "%0.6ff%da%da%da%d " % \
					(d[j][k], link[l][1], link[l][0], j, k)
			first = False
	line += "<= %0.6f\n" % cm[link[l][0]][link[l][1]]
	line_r += "<= %0.6f\n" % cm[link[l][1]][link[l][0]]
	f.write(line)
	f.write(line_r)

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

# fij(l)/cap(l) - supl(i,j) + slowl(i,j) = pl(i,j)
for i in range(ll):
	for j in range(node):
		for k in range(node):
			if j == k:
				continue
			line = "%0.6ff%da%da%da%d + %0.6ff%da%da%da%d - sup%da%da%d + slow%da%da%d " % \
					(1/cm[link[i][0]][link[i][1]], link[i][0], link[i][1], j, k,\
					1/cm[link[i][0]][link[i][1]], link[i][1], link[i][0], j, k,\
					i, j, k, i, j, k)
			if j == k:
				line += " = 0\n"
			else:
				line += " - p%da%da%d = 0\n" % (i, j, k)
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




for i in range(ll):
	line = ""
	first = True
	for j in range(node):
		for k in range(node):
			if b[j][k] == 0:
				pass
			elif b[j][k] > 0:
				if not first:
					line += "+ "
				line += "%0.6fsup%da%da%d - %0.6fslow%da%da%d " % \
					(b[j][k], i, j, k, a[j][k], i, j, k)
				first = False
			else:
				if not first:
					line += "- "
				line += "%0.6fsup%da%da%d + %0.6fslow%da%da%d " % \
					(-b[j][k], i, j, k, -a[j][k], i, j, k)
				first = False
	line += "<= 0\n"
	f.write(line)
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
				f.write("0 <= slow%da%da%d\n" % (i, j, k))
				f.write("0 <= sup%da%da%d\n" % (i, j, k))
			else:
				f.write("0 <= p%da%da%d <= 0\n" % (i, j, k))
'''
# fij(l)/cap(l) - supl(i,j) + slowl(i,j) = pl(i,j)
for i in range(ll):
	for j in range(node):
		for k in range(node):
			if j == k:
				continue
			line = "%0.4ff%da%da%da%d + %0.4ff%da%da%da%d - r <= 0\n" % \
					(1/cm[link[i][0]][link[i][1]], link[i][0], link[i][1], j, k,\
					1/cm[link[i][0]][link[i][1]], link[i][1], link[i][0], j, k)
			f.write(line)
'''

# End
f.write("end\n")
f.close()


