card = [[155.52, 60],[1244.16, 100],[2488.32, 140],[9953.28, 174]]
topology_template = "../topology/final/%s-final-%s-%s-topology"
power_file = "result-power"

for topo in ['abilene', 'geant']:
    for w in ['0', '1']:
        for alpha in ['80', '85', '90', '95', '100']:
            topology = topology_template % (topo, w, alpha)

            f = open(topology, "r")
            token = f.readline().strip().split(' ')
            node_n = int(token[0])
            link_n = int(token[1])

            power_sum = 0
            line = f.readline()
            while line:
                token = line.strip().split(' ')
                s = int(token[0])
                d = int(token[1])
                c = float(token[2])

                while True:
                    if c > card[3][0]:
                        c -= card[3][0]
                        power_sum += card[3][1]
                    elif c > card[2][0]:
                        c -= card[2][0]
                        power_sum += card[2][1]
                    elif c > card[1][0]:
                        c -= card[1][0]
                        power_sum += card[1][1]
                    elif c > card[0][0]:
                        c -= card[0][0]
                        power_sum += card[0][1]
                    else:
                        power_sum += card[0][1]
                        break

                line = f.readline()
            f.close()

            f = open(power_file, "a")
            f.write("%s-%s-%s %d\n" % (topo, w, alpha, power_sum))
            f.close()


