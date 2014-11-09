files = ['1221', '1239', '1755', '3257', '3967', '6461']

for name in files:
    f  = open("../data/isp/%s/weights.intra" % name, 'r');

    nodes_set = set()
    links_set = set()
    for line in f:
        tokens = line.split(' ')
        nodes_set.add(tokens[0])
        nodes_set.add(tokens[1])

        links_set.add(line.strip())

    num = 0
    nodes = {}
    links = set()
    for n in nodes_set:
        nodes[n] = num
        num = num + 1

    for line in links_set:
        tokens = line.split(' ')

        c = float(tokens[2])
        s = int(nodes[tokens[0]])
        d = int(nodes[tokens[1]])
        
        if s < d:
            links.add((s, d, c))
        else:
            links.add((d, s, c))


    f = open("../topology/isp/%s-topology" % name, 'w');
    f.write('%d %d\n' % (len(nodes), len(links)));
    for s, d, c in links:
        f.write('%d %d %.2f\n' % (s, d, c))
