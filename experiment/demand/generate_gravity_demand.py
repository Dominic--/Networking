import os
import random

topology_template = '../topology/connected/%s-connected-topology'
demand_template = '../demand/gravity-%s/%0.1f/%d.txt'
dir_template = '../demand/gravity-%s/%0.1f'
files = 1000
topology_name = ['cernet2']

for w in [1.5]:
    for t in topology_name:
        direcotry = '../demand/gravity-%s/%0.1f' % (t, w)
        os.system("mkdir %s" % direcotry)

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

        for n in range(0, files):
            demand = demand_template % (t, w, n)
            f = open(demand, "w")
            f.write("%d\n" % (node_n * node_n - node_n))

            for s in range(node_n):
                for d in range(node_n):
                    if s == d:
                        continue

                    f.write("%d %d %0.3f\n" % (s, d, random.uniform(nodes[s] * nodes[d] / w, nodes[s] * nodes[d] * w)))
                    #print "%d %d %0.3f\n" % (s, d, random.uniform(nodes[s] * nodes[d] / w, nodes[s] * nodes[d] * w))

            f.close()

