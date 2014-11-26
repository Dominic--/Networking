import parse_xml as xml
import global_route_with_tm_bound as cplex

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

files = ['abilene']
for name in files:
    topology = "../topology/connected/%s-connected-topology" % name
    f = open(topology, "r")
    
    line = f.readline().strip()
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

    w = 1.5
    temporary_topology = topology
    remove_links = []
    remove_n = 0
    while True:
        cplex.generate_sol(topology, [0, w], True)  
        link_order = xml.get_link_order("global_opt_cplex_output.sol", topology)

        have_remove = False
        for l in link_order:
            ls, ld = l

            temp_c = links[ls][ld]
            links[ls][ld] = 0
            links[ld][ls] = 0

            if not is_connected(links, nodes_n):
                links[ls][ld] = temp_c
                links[ld][ls] = temp_c
            else:
                remove_links.append(l)
                remove_n += 1
        
                temporary_topology = "../topology/final/%s-final-topology-%d" % (name, remove_n)
                f = open(temporary_topology, "w")
                f.write('%d %d\n' % (nodes_n, links_n-remove_n))

                for s in range(nodes_n):
                    for d in range(s, nodes_n):
                        if links[s][d] != 0:
                            f.write('%d %d %.2f\n' % (s, d, links[s][d]))
                f.close()

                f = open("../topology/remove/%s-remove-%d-links" % (name, remove_n), "w")
                for l in remove_links:
                    f.write('%d %d\n' % (l[0], l[1]))
                f.close()

                break

        if remove_n == (likns_n - nodes_n + 1):
            break