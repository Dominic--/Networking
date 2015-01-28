import parse_xml as xml
import global_route_with_tm_bound as cplex

# check the graph represented by links if connected.
# nodes is the set of visited nodes, stack is the stack of to-be-visited nodes
# every time pop a node from stack, visit it, 
# and finally check if all the nodes is visited.
def is_connected(links, nodes_n):
    stack = [0]
    nodes = set()
    
    while len(stack) > 0:
        from_node = stack.pop()
        nodes.add(from_node)
        for to_node in range(nodes_n):
            if links[from_node][to_node] != 0 and to_node not in nodes:
                stack.append(to_node)

    if len(nodes) == nodes_n:
        return True
    else:
        return False



#files = ['abilene', 'geant']
power_models = {155.0:60, 1240.0:100, 2480.0:140, 9920:174}
power_model = [60, 100, 140, 174]

files = ['abilene', 'cernet2', 'geant']
for name in files:
    topology = "../topology/connected/%s-connected-topology" % name
    f = open(topology, "r")
    
    line = f.readline().strip()
    nodes_n = int(line.split(' ')[0])
    links_n = int(line.split(' ')[1])

    links = [[0 for i in range(nodes_n)] for j in range(nodes_n)]
    powers = []
    for line in f:
        tokens = line.strip().split(' ')

        s = int(tokens[0])
        d = int(tokens[1])
        c = float(tokens[2])

        total = 0
        if c <= 155.0:
            total = power_model[0]
        elif c <= 1240.0:
            total = power_model[1]
        elif c <= 2480.0:
            total = power_model[2]
        elif c <= 9920.0:
            total = power_model[3]

        powers.append((s,d,total))

        links[s][d] = c
        links[d][s] = c
    f.close()

    for i in range(0, len(powers) - 1):
        for j in range(i+1, len(powers)):
            si, di, pi = powers[i]
            sj, dj, pj = powers[j]
            
            if pi < pj:
                powers[i] = (sj, dj, pj)
                powers[j] = (si, di, pi)


    temporary_topology = topology
    remove_links = []
    remove_n = 0
    while True:
        for ls,ld,lp in powers:

            temp_c = links[ls][ld]
            links[ls][ld] = 0
            links[ld][ls] = 0

            if not is_connected(links, nodes_n):
                links[ls][ld] = temp_c
                links[ld][ls] = temp_c
            else:
                remove_links.append([ls, ld])
                powers.remove((ls, ld, lp))
                remove_n += 1
        
                temporary_topology = "../topology/final/%s-final-topology-%d-power" % (name, remove_n)
                f = open(temporary_topology, "w")
                f.write('%d %d\n' % (nodes_n, links_n-remove_n))

                for s in range(nodes_n):
                    for d in range(s, nodes_n):
                        if links[s][d] != 0:
                            f.write('%d %d %.2f\n' % (s, d, links[s][d]))
                f.close()

                f = open("../topology/remove/%s-remove-%d-links-power" % (name, remove_n), "w")
                for l in remove_links:
                    f.write('%d %d\n' % (l[0], l[1]))
                f.close()

                break

        if remove_n == (links_n - nodes_n + 1):
            break
