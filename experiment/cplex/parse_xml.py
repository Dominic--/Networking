import xml.dom.minidom
import random
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
            variables[node.getAttribute("name")] = float(node.getAttribute("value"))

    return variables

def print_cap(result, topology):
    f = open(topology);

    node = (int)(f.readline().strip().split(" ")[0])

    cm = [([0] * node) for i in range(node)]
    link = list()
    line = f.readline()
    while line:
        s = line.rstrip().split(" ")
        cm[int(s[0])][int(s[1])] = (float)(s[2])
        cm[int(s[1])][int(s[0])] = (float)(s[2])
        link.append([int(s[0]),int(s[1])])
        line = f.readline()
    f.close()
    ll = len(link)

    f = open(result)
    xml_string = f.read().replace('\n', '')
    f.close()

    value = dict()
    dom = xml.dom.minidom.parseString(xml_string)
    for node in dom.getElementsByTagName("variable"):
        value[node.getAttribute("name")] = float(node.getAttribute("value"))

    for i in range(ll):
        tmp = 0
        for j in range(ll):
            #print "%s %f" % ('pai%da%d' % (i, j), value['pai%da%d' % (i, j)])
            tmp += (cm[link[j][0]][link[j][1]] * value['pai%da%d' % (i, j)])
        #print "%d : %f" % (i, tmp)

def filter(st_paths, links):
    routes = {}
    num = 0
    for key in st_paths.keys():
        value = st_paths[key]
        random_sum = 0
        for v in value:
            random_sum += v[1]
        #print "%d : %f" % (num, random_sum)
        num += 1
        random_num = random.uniform(0, random_sum)
        for v in value:
            if random_num < v[1]:
                routes[key] = [v[0], random_sum]
                break
            else:
                random_num -= v[1]
    #print routes

    for r in routes:
        v = routes[r]
        for i in range(len(v[0]) - 1):
            a = 0
            b = 0
            if v[0][i] > v[0][i+1]:
                a = v[0][i+1]
                b = v[0][i]
            else:
                a = v[0][i]
                b = v[0][i+1]
            if (a,b) not in links:
                links[(a,b)] = 1
            else :
                links[(a,b)] += 1

    #print links

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

    #print st_paths[(9,5)]
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

    #print "-------------------------------------"
    #print variables[(9,5)]
    #print "-------------------------------------"
    return route_from_variables(variables)

def get_route_with_demand(file_name, demand):
    f = open(file_name)
    xml_string = f.read().replace('\n', '')
    f.close()

    f = open(demand)
    dd = dict()
    line = f.readline()
    line = f.readline()
    while line:
        s = line.rstrip().split(' ')
        dd[int(s[0]), int(s[1])] = (float)(s[2])
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
                if (s[2],s[3]) not in dd.keys():
                    variables[(s[2], s[3])].append([s[0], s[1], 0])
                else:
                    variables[(s[2], s[3])].append([s[0], s[1], float(node.getAttribute("value")) * dd[s[2], s[3]]])

    return route_from_variables(variables)

def get_link_order_attr(solution, topology):
    st_paths = get_route(solution)

    links = {}
    for i in range(300):
        filter(st_paths, links)

    f = open(topology, "r")
    line = f.readline()
    line = f.readline()

    cm = {}
    while line:
        token = line.strip().split(" ")
        ls = int(token[0])
        ld = int(token[1])
        lc = float(token[2])

        cm[(ls,ld)] = lc

        line = f.readline()
    f.close()

    link_order = []
    for key in cm:
        s,d = key
        link_order.append([(s, d), cm[(s,d)] / links[(s,d)]])
    
    for i in range(len(link_order) - 1):
        for j in range(i+1, len(link_order)):
            if link_order[i][1] < link_order[j][1]:
                temp_s, temp_d = link_order[i][0]
                temp_c = link_order[i][1]

                link_order[i][0] = link_order[j][0]
                link_order[i][1] = link_order[j][1]

                link_order[j][0] = (temp_s, temp_d)
                link_order[j][1] = temp_c
    

    lo = []
    for l in link_order:
        s, d = l[0]
        lo.append([(s,d), cm[(s,d)], links[(s,d)]])

    return lo

def get_link_order(solution, topology):
    st_paths = get_route(solution)

    links = {}
    for i in range(300):
        filter(st_paths, links)

    f = open(topology, "r")
    line = f.readline()
    line = f.readline()

    cm = {}
    while line:
        token = line.strip().split(" ")
        ls = int(token[0])
        ld = int(token[1])
        lc = float(token[2])

        cm[(ls,ld)] = lc

        line = f.readline()
    f.close()

    link_order = []
    for key in cm:
        s,d = key
        link_order.append([(s, d), cm[(s,d)] / links[(s,d)]])
    
    for i in range(len(link_order) - 1):
        for j in range(i+1, len(link_order)):
            if link_order[i][1] < link_order[j][1]:
                temp_s, temp_d = link_order[i][0]
                temp_c = link_order[i][1]

                link_order[i][0] = link_order[j][0]
                link_order[i][1] = link_order[j][1]

                link_order[j][0] = (temp_s, temp_d)
                link_order[j][1] = temp_c
    

    lo = []
    for l in link_order:
        lo.append(l[0])

    return lo

if __name__ == '__main__':
    #print_cap('test2.xml', '../topology/connected/geant-connected-topology')
    #topology = '../topology/connected/geant-connected-topology'
    #st_paths = get_route('test2.xml')

    topology = '../topology/connected/abilene-connected-topology'

	
    get_link_order('abilene-connected-cplex.sol', topology)
