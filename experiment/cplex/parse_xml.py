import xml.dom.minidom
from deep_first_search_path import *
import re

# objective value of cplex
def get_object(file_name):
	f = open(file_name)
	xml_string = f.read().replace('\n', '')
	f.close()

	dom = xml.dom.minidom.parseString(xml_string)
	header = dom.getElementsByTagName("header")[0]

	return float(header.getAttribute("objectiveValue"))

def get_variables(file_name):
	f = open(file_name)
	xml_string = f.read().replace('\n', '')
	f.close()

	dom = xml.dom.minidom.parseString(xml_string)

	variables = dict()
	for node in dom.getElementsByTagName("variable"):
		if node.getAttribute("name").startswith("f"):
			variables[node.getAttribute("name")] = \
					float(node.getAttribute("value"))

	return variables

def route_from_variables(variables):
    st_paths = {}
    for key in variables.keys():
        value = variables[key]
        g = Graph()
        s,t = key
        g.add_node(s)
        g.add_node(t)
        for v in value:
            g.add_node(v[0])
            g.add_node(v[1])
            g.add_edge((v[0], v[1], v[2]))
        st_paths[key] = g.find_path(s, t)

    return st_paths
	
def get_route(file_name):
	f = open(file_name)
	xml_string = f.read().replace('\n', '')
	f.close()

	dom = xml.dom.minidom.parseString(xml_string)
	
	p = re.compile('\d+')

	variables = dict()
	for node in dom.getElementsByTagName("variable"):
		if node.getAttribute("name").startswith("f"):
			
			name = node.getAttribute("name")
			s = p.findall(name)
			s = [int(i) for i in s]
			if not (s[2], s[3]) in variables:
				variables[(s[2], s[3])] = []
			
			if float(node.getAttribute("value")) != 0:
				variables[(s[2], s[3])].append([s[0], s[1], float(node.getAttribute("value"))])

	return route_from_variables(variables)

def get_route_with_demand(file_name, demand):
	f = open(file_name)
	xml_string = f.read().replace('\n', '')
	f.close()

	f = open(demand)
	node = (int)(f.readline().rstrip())
	dd = [([0] * node) for i in range(node)]
	line = f.readline()
	while line:
		s = line.rstrip().split(' ')
		dd[int(s[0])][int(s[1])] = (float)(s[2])
		line = f.readline()
	f.close()


	dom = xml.dom.minidom.parseString(xml_string)
	
	p = re.compile('\d+')

	variables = dict()
	for node in dom.getElementsByTagName("variable"):
		if node.getAttribute("name").startswith("f"):
			
			name = node.getAttribute("name")
			s = p.findall(name)
			s = [int(i) for i in s]
			if not (s[2], s[3]) in variables:
				variables[(s[2], s[3])] = []
			
			if float(node.getAttribute("value")) != 0:
				variables[(s[2], s[3])].append([s[0], s[1], float(node.getAttribute("value")) * dd[s[2]][s[3]]])

	return route_from_variables(variables)
	
