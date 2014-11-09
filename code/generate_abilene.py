f  = open("abilene/topo-2003-04-10.txt", 'r');
fo = open("graph", 'w');

nodes = {}
links = []
num = 0;
line_n = 0
for line in f:
    line_n = line_n + 1
    if line_n >= 3 and line_n <= 14:
        s = line.split(' ')
        nodes[s[0].strip()] = num
        num = num + 1
    elif line_n >= 19 and line_n <= 48:
        s = line.split('\t')
        ss = s[2].split(' ')
        links.append((nodes[s[0].strip()], nodes[s[1].strip()], ss[0].strip()))

fo.write('%d %d\n' % (len(nodes), len(links)));
for s, d, c in links:
    fo.write('%d %d %s\n' % (s, d, c))
