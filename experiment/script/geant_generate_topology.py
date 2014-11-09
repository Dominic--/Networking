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


f = open("../topology/geant-topology", "w")
f.write('%d %d\n' % (len(nodes), len(links)))
for s,d in links:
    f.write('%d %d %d\n' % (s, d, links[(s,d)]))



