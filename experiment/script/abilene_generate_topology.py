f  = open("../data/abilene/topo-2003-04-10.txt", 'r');

nodes = {}
links = set()
num = 0;
line_n = 0
for line in f:
    line_n = line_n + 1
    if line_n >= 3 and line_n <= 14:
        tokens = line.split('\t')
        nodes[tokens[0].strip()] = num
        num = num + 1
    elif line_n >= 19 and line_n <= 48:
        tokens = line.split('\t')
        capacity = tokens[2].split(' ')[0]

        if int(nodes[tokens[0]]) > int(nodes[tokens[1]]):
            links.add((int(nodes[tokens[1]]), int(nodes[tokens[0]]), capacity))
        else:
            links.add((int(nodes[tokens[0]]), int(nodes[tokens[1]]), capacity))


f = open("../topology/abilene-topology", 'w');
f.write('%d %d\n' % (len(nodes), len(links)));
for s, d, c in links:
    f.write('%d %d %s\n' % (s, d, c))


