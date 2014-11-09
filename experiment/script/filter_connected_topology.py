files = ['geant', 'abilene', '1221', '1239', '1755', '3257', '3967', '6461']

for name in files:
    f  = open("../topology/temp/%s-topology" % name, 'r');
    
    line = f.readline()
    nodes_n = int(line.split(' ')[0])
    links_n = int(line.split(' ')[1])

    links = [[0 for i in range(nodes_n)] for j in range(nodes_n)]
    for line in f:
        tokens = line.strip().split(' ')

        s = int(tokens[0])
        d = int(tokens[1])
        c = float(tokens[2])

        links[s][d] = c
        links[d][s] = c
    f.close()

    stack = [0]
    nodes = set()
    while len(stack) > 0:
        from_node = stack.pop()
        nodes.add(from_node)
        for to_node in range(nodes_n):
            if links[from_node][to_node] != 0 and to_node not in nodes:
                stack.append(to_node)

    num = 0
    for s in range(nodes_n):
        for d in range(s, nodes_n):
            if links[s][d] != 0 and s in nodes:
                num = num + 1

    f = open('../topology/connected/%s-connected-topology' % name, 'w')
    f.write('%d %d\n' % (len(nodes), num))

    new_nodes = sorted(nodes)
    old_map_new = {}
    num = 0
    for n in range(0, nodes_n):
        if n in nodes:
            old_map_new[n] = num
            num = num + 1

    for s in range(nodes_n):
        for d in range(s, nodes_n):
            if links[s][d] != 0 and s in nodes:
                f.write('%d %d %.2f\n' % (old_map_new[s], old_map_new[d], links[s][d]))
    f.close()
