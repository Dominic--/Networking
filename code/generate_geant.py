import xml.etree.cElementTree as ET

def find_in_tree(tree, node):
    found = tree.iterfind(node)
    if found == None:
        print "No %s in file" % node
        found = []
    return found

dom = ET.parse(open("geant/geant-topology.xml", "r"))
root = dom.getroot()

nodes = find_in_tree(root, "nodes")
print nodes

for n in find_in_tree(nodes, "node"):
    print n.get('id')

