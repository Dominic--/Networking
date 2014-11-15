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

    def nodes(self):
        return self.node_neighbors.keys()

    def dfs_path(self, s, v):
        self.visited = {}
        def find_max(q):
            m = 0
            key = 0
            for i in q:
                if q[i] > m:
                    m = q[i]
                    key = i
            return key

        path = []
        queue = {}
        for n in self.nodes():
            queue[n] = 0

        queue[s] = 100000
        while True:
            node = find_max(queue)
            w = queue[node]
            path.append(node)

            if node == v:
                return path
            else:
                for n in self.node_neighbors[node]:
                    if n[0] not in self.visited:
                        weight = 0
                        if w > n[1]:
                            weight = n[1]
                        else:
                            weight = w

                        if weight > queue[n[0]]:
                            queue[n[0]] = weight
                queue.pop(node)

            self.visited[node] = True
		
    def find_path(self, s, v):
        paths = []
        path = []
        def dfs(node):
            self.visited[node] = True
            path.append(node)

            if node == v:
                min_weight = 10000
                for i in range(len(path) - 1):
                    for n in self.node_neighbors[path[i]]:
                        if n[0] == path[i+1] and min_weight > n[1]:
                            min_weight = n[1]
                
                for i in range(len(path) - 1):
                    for n in self.node_neighbors[path[i]]:
                        if n[0] == path[i+1]:
                            n[1] -= min_weight
                
                paths.append([[i for i in path], min_weight])
                path.remove(node)
                
                self.visited.pop(node, None)
                return

            for n in self.node_neighbors[node]:
                if not n[0] in self.visited and n[1] > 0:
                    dfs(n[0])

            self.visited.pop(node, None)
            path.remove(node)
                        
        dfs(s)

        return paths

if __name__ == '__main__':
	g = Graph()
	g.add_nodes([i for i in range(4)])
	g.add_edge((0, 1, 2))
	g.add_edge((0, 2, 5))
	g.add_edge((1, 3, 3))
	g.add_edge((2, 1, 1))
	g.add_edge((2, 3, 4))
	print("nodes:", g.nodes())

	#paths = g.find_path(0, 3)
	path = g.dfs_path(0, 3)
	print(path)
