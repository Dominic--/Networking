import random

def generate_cplex_lp_file(topology, outfile, bound, is_gravity):
    f = open(topology)

    # Node
    node = (int)(f.readline().rstrip().split(' ')[0])
    nodes = [0 for i in range(node)]

    # Capacity Matrix
    # Link Set
    cm = [([0] * node) for i in range(node)]
    link = list()
    line = f.readline()
    while line:
        s = line.rstrip().split(" ")
        cm[int(s[0])][int(s[1])] = (float)(s[2])
        cm[int(s[1])][int(s[0])] = (float)(s[2])

        nodes[int(s[0])] += float(s[2])
        nodes[int(s[1])] += float(s[2])

        link.append([int(s[0]), int(s[1])])
        line = f.readline()
    f.close()
    ll = len(link)

    a = [([0] * node) for i in range(node)]
    b = [([0] * node) for i in range(node)]

    for s in range(node):
        for d in range(node):
            if s != d:
                if is_gravity:
                    b[s][d] = nodes[s] * nodes[d] * bound[1]
                    a[s][d] = nodes[s] * nodes[d] / bound[1]
                else:
                    a[s][d] = bound[0]
                    b[s][d] = bound[1]

    # Begin
    f = open(outfile, 'w')
    f.write("Min\nr\nsubject to\n")


    # Generate CPLEX
    # f(l1, l2, s, t) is routing
    for i in range(node):
        for j in range(node):
            if i == j:
                continue
            for k in range(node):
                line = ""
                first = True
                for l in range(ll):
                    # l, k is the tail
                    if k == link[l][1]:
                        if not first:
                            line += "+ f%da%da%da%d " % (link[l][0], link[l][1], i, j)
                        else:
                            line += "f%da%da%da%d " % (link[l][0], link[l][1], i, j)
                            first = False

                    # l, k is the head
                    if k == link[l][0]:
                        if not first:
                            line += "- f%da%da%da%d " % (link[l][0], link[l][1], i, j)
                        else:
                            line += "-f%da%da%da%d " % (link[l][0], link[l][1], i, j)
                            first = False
                        
                    # -l, k is the tail
                    if k == link[l][0]:
                        if not first:
                            line += "+ f%da%da%da%d " % (link[l][1], link[l][0], i, j)
                        else:
                            line += "f%da%da%da%d " % (link[l][1], link[l][0], i, j)
                            first = False
        
                    # -l, k is the head
                    if k == link[l][1]:
                        if not first:
                            line += "- f%da%da%da%d " % (link[l][1], link[l][0], i, j)
                        else:
                            line += "-f%da%da%da%d " % (link[l][1], link[l][0], i, j)
                            first = False
                
                if k == j:
                    line += "= 1\n"
                elif k == i:
                    line += "= -1\n"
                else:
                    line += "= 0\n"
                f.write(line)

    '''
    for l in range(ll):
        line = ""
        first = True
        for j in range(node):
            for k in range(node):
                if j == k:
                    continue
                if not first:
                    line += "+ "
                line += "%0.6ff%da%da%da%d " % \
                        (d[j][k], link[l][0], link[l][1], j, k)
                first = False
                if not first:
                    line += "+ "
                line += "%0.6ff%da%da%da%d " % \
                        (d[j][k], link[l][1], link[l][0], j, k)
                first = False
        line += "<= %0.6f\n" % cm[link[l][0]][link[l][1]]
        f.write(line)
    '''

    # cap(m)pai(l,m) <= r
    for i in range(ll):
        line = ""
        for j in range(ll):
            if j != 0:
                line += "+ "
            line += "%0.6fpai%da%d " % (cm[link[j][0]][link[j][1]], i, j)
        line += " - r <= 0\n"
        f.write(line)
        #break


    # fij(l)/cap(l) - supl(i,j) + slowl(i,j) = pl(i,j)
    for i in range(ll):
        for j in range(node):
            for k in range(node):
                if j == k:
                    continue
                line = "%0.6ff%da%da%da%d + %0.6ff%da%da%da%d - sup%da%da%d + slow%da%da%d " % \
                        (1/cm[link[i][0]][link[i][1]], link[i][0], link[i][1], j, k,\
                        1/cm[link[i][0]][link[i][1]], link[i][1], link[i][0], j, k,\
                        i, j, k, i, j, k)
                if j == k:
                    line += " = 0\n"
                else:
                    line += " - p%da%da%d = 0\n" % (i, j, k)
                f.write(line)
                #break
            #break
        #break

    # pai(l, link-of(e)) + pl(i,j) - pl(i, k) >= 0
    for i in range(ll):
        for j in range(node):
            for k in range(ll):
                line = "pai%da%d + p%da%da%d - p%da%da%d >= 0\n" % \
                        (i, k, i, j, link[k][0], i, j, link[k][1])
                line += "pai%da%d + p%da%da%d - p%da%da%d >= 0\n" % \
                        (i, k, i, j, link[k][1], i, j, link[k][0])
                f.write(line)
                #break
            #break
        #break


    for i in range(ll):
        line = ""
        first = True
        for j in range(node):
            for k in range(node):
                if b[j][k] == 0:
                    pass
                elif b[j][k] > 0:
                    if not first:
                        line += "+ "
                    line += "%0.6fsup%da%da%d - %0.6fslow%da%da%d " % \
                        (b[j][k], i, j, k, a[j][k], i, j, k)
                    first = False
                else:
                    if not first:
                        line += "- "
                    line += "%0.6fsup%da%da%d + %0.6fslow%da%da%d " % \
                        (-b[j][k], i, j, k, -a[j][k], i, j, k)
                    first = False
        line += "<= 0\n"
        f.write(line)
        #break
                    
    # bounds
    f.write("bound\n")
    for i in range(ll):
        for j in range(ll):
            f.write("0 <= pai%da%d\n" % (i, j))

    for i in range(ll):
        for j in range(node):
            for k in range(node):
                if j != k:
                    f.write("0 <= p%da%da%d\n" % (i, j, k))
                    f.write("0 <= f%da%da%da%d <= 1\n" % (link[i][0], link[i][1], j, k))
                    f.write("0 <= f%da%da%da%d <= 1\n" % (link[i][1], link[i][0], j, k))
                    f.write("0 <= slow%da%da%d\n" % (i, j, k))
                    f.write("0 <= sup%da%da%d\n" % (i, j, k))
                else:
                    f.write("0 <= p%da%da%d <= 0\n" % (i, j, k))

    # End
    f.write("end\n")
    f.close()


