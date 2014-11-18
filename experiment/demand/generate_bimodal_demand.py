import random

topology_template = '../topology/connected/%s-connected-topology'
demand_template = '../demand/bimodal-%s/%d.txt'
files = 1000
topology_name = ['abilene', 'geant']

for t in topology_name:
    topology = topology_template % t

    f = open(topology, "r")
    token = f.readline().strip().split(' ')
    node_n = int(token[0])
    link_n = int(token[1])

    random_range = 0
    line = f.readline()
    while line:
        token = line.strip().split(' ')
        random_range += float(token[2])

        line = f.readline()
    f.close()

    random_range = random_range / link_n
    print random_range
    for n in range(files):
        demands = dict()

        od_sum = int(random.uniform(1, node_n * node_n - node_n + 1))
        od_num = 0
        #print n, od_num, od_sum
        while True:
            src = int(random.uniform(0, node_n))
            dst = int(random.uniform(0, node_n))
            
            if src == dst:
                continue

            if (src, dst) in demands:
                continue

            if (src,dst) not in demands:
                demands[src, dst] = random.uniform(0, random_range)
            
            od_num += 1
            if od_num == od_sum:
                break
        
        demand = demand_template % (t, n)
        f = open(demand, "w")
        f.write("%d\n" % len(demands))
        for s,d in demands:
            f.write("%d %d %0.2f\n" % (s, d, demands[s,d]))

        f.close()

