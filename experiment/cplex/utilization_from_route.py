import random

def get_utilization(topology, routes, loop):
    # init cm and dd
    f = open(topology)
    line = f.readline().rstrip().split(' ')
    node = (int)(line[0])
    links = (int)(line[1])
    cm = [([0] * node) for i in range(node)]

    line = f.readline()
    while line:
        s = line.rstrip().split(' ')
        cm[int(s[0])][int(s[1])] = float(s[2])
        cm[int(s[1])][int(s[0])] = float(s[2])
        line = f.readline()
    f.close()

    min_loop = 10000
    for l in range(loop):
        st_path = {}
        for key in routes.keys():
            value = routes[key]
            random_sum = 0
            for v in value:
                random_sum += v[1]
            random_num = random.uniform(0, random_sum)
            for v in value:
                if random_num < v[1]:
                    st_path[key] = [v[0], random_sum]
                else:
                    random_num -= v[1]

        dd = [([0] * node) for i in range(node)]

        for key in st_path.keys():
            v = st_path[key]
            path = v[0]
            weight = v[1]
            for i in range(len(path) - 1):
                dd[path[i]][path[i+1]] += weight
                dd[path[i+1]][path[i]] += weight

        link_u = 0
        for i in range(node):
            for j in range(node):
                if cm[i][j] != 0 and dd[i][j] / cm[i][j] > link_u:
                    link_u = dd[i][j] / cm[i][j]

        if link_u < min_loop:
            min_loop = link_u

        #print('New Utilization For %d: %f' % (l, link_u))

    return link_u
