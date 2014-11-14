# Correpond Node to City
# && Change to undirected graph
# && remove 1-connected node

import re
# Topology File Name
topology = "1239.weights.intra"

# Linked in slef-city will not be included
# Input data formated:
#		City,+Country City,+Country weights
origin = list()
f = open(topology)
line = f.readline()
while line:
	s = line.rstrip().split(" ")
	src = s[0].split(",")
	dest = s[1].split(",")
	ss = re.sub('[0-9]+', '', src[0])
	dd = re.sub('[0-9]+', '', dest[0])
	if ss != dd:
		origin.append([ss, dd, s[2]])
	line = f.readline()

#print(len(origin))

# Merge two links whose OD pairs are same
# Change directed to undirected
cities = set()
links = set()
result = list()
for o in origin:
	weight = 0
	for r in origin:
		if o[0] == r[0] and o[1] == r[1]:
			weight += (float)(r[2])
	cities.add(o[0])
	if '%s+%s' % (o[0], o[1]) not in links and \
			'%s+%s' % (o[1], o[0]) not in links:
		links.add('%s+%s' % (o[0], o[1]))
		result.append([o[0], o[1], weight])

print(len(result))
print(len(cities))

# Rename City Name to Index
name_map = dict()
index = 0
for i in sorted(cities):
	name_map[i] = index
	index += 1

for i in result:
	for j in range(2):
		i[j] = name_map[i[j]]


# Remove node whose degee equal 1
reduced = list()
matrix = [([0] * len(cities)) for i in range(len(cities))]
for r in result:
	if r[0] < r[1]:
		matrix[r[0]][r[1]] = r[2]
	else:
		matrix[r[1]][r[0]] = r[2]

itr = 0
node = len(cities)
while itr < node:
	remove = 0
	for i in range(node):
		if matrix[itr][i] > 0:
			remove += 1
		if matrix[i][itr] > 0:
			remove += 1
	if remove == 1:
		for i in range(node):
			matrix[itr][i] = 0
			matrix[i][itr] = 0
		itr = 0
	else:
		itr += 1

cities = set()
for i in range(node):
	for j in range(node):
		if matrix[i][j] != 0:
			reduced.append([i, j, matrix[i][j]])
			cities.add(i)
			cities.add(j)

#print(len(reduced))

# Rename reduced node name
name_map = dict()
index = 0
for i in cities:
	name_map[i] = index
	index += 1

for i in reduced:
	for j in range(2):
		i[j] = name_map[i[j]]

print(len(cities))
print(len(reduced))

# Output
t = "weights.intra.new"
f = open(t, 'w')
f.write("%d\n" % len(cities))
for r in reduced:
	f.write("%s %s %0.1f\n" % (r[0], r[1], r[2]))
f.close()
