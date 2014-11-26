import random

topology_template = '../topology/connected/%s-connected-topology'
demand_template = '../demand/gravity-%s/%d.txt'
files = 1000
w = 1.5
topology_name = ['abilene', 'geant']

for t in topology_name:
    topology = topology_template % t

    f = open(topology, "r")
    token = f.readline().strip().split(' ')
    node_n = int(token[0])
    link_n = int(token[1])

    random_range = 0
    nodes = [0 for i in range(node_n)]
    line = f.readline()
    while line:
        token = line.strip().split(' ')
        nodes[int(token[0])] += float(token[2])
        nodes[int(token[1])] += float(token[2])
        random_range += float(token[2])

        line = f.readline()
    f.close()

    '''
    first_value = 0
    second_value = 0
    for i in range(node_n):
        if first_value < nodes[i]:
            second_value = first_value

            first_value = nodes[i]
        elif second_value < nodes[i]:
            second_value = nodes[i]

    random_range = random_range / link_n
    random_base = random_range / first_value / second_value
    random_base = 0.001
    '''

    for n in range(files):
        demand = demand_template % (t, n)
        f = open(demand, "w")
        f.write("%d\n" % (node_n * node_n - node_n))

        for s in range(node_n):
            for d in range(node_n):
                if s == d:
                    continue

                f.write("%d %d %0.3f\n" % (s, d, random.uniform(nodes[s] * nodes[d] / w, nodes[s] * nodes[d] * w)))

        f.close()

