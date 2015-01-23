class Graph(object):

    def __init__(self,*args,**kwargs):
        self.node_neighbors = {} 
        self.visited = {}

    def add_nodes(self,nodelist): 
        for node in nodelist: 
            self.add_node(node)
    
    def add_node(self,node): 
        if not node in self.nodes(): 
            self.node_neighbors[node] = [] 

    def add_edge(self,edge):
        u,v,w = edge
        if(v not in self.node_neighbors[u]):
            self.node_neighbors[u].append([v, w])
        # debug for the random sum is not always equal to 0
        #if(u not in self.node_neighbors[v]):
        #    self.node_neighbors[v].append([u, w])

    def nodes(self):
        return self.node_neighbors.keys()

    #multi dfs path
    def multi_dfs_path(self, s, v):
        self.visited = {}
        def find_max(q):
            m = 0
            key = 0
            for i in q:
                if q[i] > m:
                    m = q[i]
                    key = i
            if m > 0:
                return key
            else:
                return None
        
        path = []
        def get_path(v, p):
            if p[v] != None:
                get_path(p[v], p)
                path.append(v)
            else:
                path.append(v)
                

        path = []
        queue = {}
        for n in self.nodes():
            queue[n] = 0

        queue[s] = 100000
        parents = {}
        parents[s] = None
        while True:
            node = find_max(queue)

            if node == None:
                return None
            w = queue[node]

            if node == v:
                get_path(v, parents)
                return path
            else:
                for n in self.node_neighbors[node]:
                    if n[0] not in self.visited:
                        weight = w
                        if w > n[1]:
                            weight = n[1]

                        if weight > queue[n[0]]:
                            queue[n[0]] = weight
                            parents[n[0]] = node

                queue.pop(node)

            self.visited[node] = True
		
    #dijkstra path
    def dfs_path(self, s, v):
        self.visited = {}
        def find_max(q):
            m = 0
            key = 0
            for i in q:
                if q[i] > m:
                    m = q[i]
                    key = i
            if m > 0:
                return key
            else:
                return None
        
        path = []
        def get_path(v, p):
            if p[v] != None:
                get_path(p[v], p)
                path.append(v)
            else:
                path.append(v)
                

        path = []
        queue = {}
        for n in self.nodes():
            queue[n] = 0

        queue[s] = 100000
        parents = {}
        parents[s] = None
        while True:
            node = find_max(queue)

            if node == None:
                return None
            w = queue[node]

            if node == v:
                get_path(v, parents)
                return path
            else:
                for n in self.node_neighbors[node]:
                    if n[0] not in self.visited:
                        weight = w
                        if w > n[1]:
                            weight = n[1]

                        if weight > queue[n[0]]:
                            queue[n[0]] = weight
                            parents[n[0]] = node

                queue.pop(node)

            self.visited[node] = True
		
    def find_path(self, s, v):
        paths = []
        path = []
        def dfs(node):
            self.visited[node] = True
            path.append(node)

            if node == v:
                min_weight = 0
                for i in range(len(path) - 1):
                    for n in self.node_neighbors[path[i]]:
                        if i == 0 and path[i+1] == n[0]:
                            min_weight = n[1]
                            continue

                        if (n[0] == path[i+1] and min_weight > n[1]):
                            min_weight = n[1]
                
                for i in range(len(path) - 1):
                    for n in self.node_neighbors[path[i]]:
                        if n[0] == path[i+1]:
                            n[1] -= min_weight

                for i in range(1, len(path)):
                    for n in self.node_neighbors[path[i]]:
                        if n[0] == path[i-1]:
                            n[1] -= min_weight
                
                
                paths.append([[i for i in path], min_weight])
                path.remove(node)
                
                self.visited.pop(node, None)
                return

            for n in self.node_neighbors[node]:
                if not n[0] in self.visited and n[1] > 0.001:
                    dfs(n[0])

            self.visited.pop(node, None)
            path.remove(node)
                        
        #for i in range(2):
            #self.visited = {}
        dfs(s)

        weight = 0
        for p,w in paths:
            weight += w

        return paths

    def find_path_without_weight(self, s, v):
        paths = []
        path = []
        def dfs(node):
            self.visited[node] = True
            path.append(node)

            if node == v:
                paths.append([[i for i in path], 0, 0])
                path.remove(node)
                
                self.visited.pop(node, None)
                return

            for n in self.node_neighbors[node]:
                if not n[0] in self.visited and len(paths) < 20:
                    dfs(n[0])

            self.visited.pop(node, None)
            path.remove(node)
                        
        dfs(s)

        return paths

if __name__ == '__main__':
	g = Graph()
	g.add_nodes([i for i in range(12)])
	g.add_edge((1, 4, 0.42))
	g.add_edge((2, 5, 0.58))
	g.add_edge((2, 8, 0.42))
	g.add_edge((3, 9, 0.14))
	g.add_edge((3, 10, 0.44))
	g.add_edge((4, 7, 0.42))
	g.add_edge((5, 6, 0.58))
	g.add_edge((6, 3, 0.58))
	g.add_edge((7, 9, 0.42))
	g.add_edge((8, 11, 0.42))
	g.add_edge((10, 9, 0.44))
	g.add_edge((11, 1, 0.42))
        print g.find_path(2, 9)
        #print(g.node_neighbors)
	#print("nodes:", g.nodes())

	#paths = g.find_path(0, 3)
	#path = g.dfs_path(0, 3)
	#path = g.dfs_path(1, 3)
	#paths = g.find_path_without_weight(2, 0)
	#print(paths)
