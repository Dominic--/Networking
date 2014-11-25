import xml.etree.ElementTree as ET

dom = ET.parse(open("../data/geant/geant-topology.xml", "r"))
root = dom.getroot()

nodes = {}
links = {}

num = 0
for ns in root.iter('nodes'):
    for n in ns.findall('node'):
        nodes[n.get('id')] = num
        num = num + 1

for ls in root.iter('links'):
    for l in ls.findall('link'):
        sd = l.get('id').split('_')
        
        capacity = 0
        for c in l.iter('metric'):
            capacity = int(c.text)

        if int(nodes[sd[0]]) < int(nodes[sd[1]]):
            links[(int(nodes[sd[0]]), int(nodes[sd[1]]))] = capacity
        else:
            links[(int(nodes[sd[1]]), int(nodes[sd[0]]))] = capacity

f = open("../data/geant/geantCap.txt", "r")
line = f.readline()
line = f.readline()
line_n = 0;
while line:
    token = line.strip().split(" ")
    for i in range(line_n, len(token)):
        if int(token[i]) != 0:
            assert(links[(line_n, i)] != 0)
            links[(line_n, i)] = int(token[i]) / 1000000
    line_n += 1
    line = f.readline()
f.close()


f = open("../topology/temp/geant-topology", "w")
f.write('%d %d\n' % (len(nodes), len(links)))
for s,d in links:
    f.write('%d %d %d\n' % (s, d, links[(s,d)]))
f.close()

f = open("../topology/final/geant-map-number", "w")
f.write("%d\n" % len(nodes))
for n in nodes:
    f.write("%s %d\n" % (n, nodes[n]))
f.close()

