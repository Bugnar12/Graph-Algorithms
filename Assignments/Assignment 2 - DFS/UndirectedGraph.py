from Exceptions import undirected_exception


class UndirectedGraph:

    def __init__(self, vertices):
        self.__dictEdges = {}
        for i in range(0, vertices):
            self.__dictEdges[i] = []

    #function that adds an edge between two vertices
    def addEdge(self, x, y):
        if x not in self.__dictEdges[y] and y not in self.__dictEdges[x]:
            self.__dictEdges[x].append(y)
            self.__dictEdges[y].append(x)
        else:
            raise undirected_exception("edge already exists")

    #function that adds a vertex
    def addVertex(self, x):
        if x in self.__dictEdges:
            raise undirected_exception("vertex already exists")
        self.__dictEdges[x] = []

    #function that returns the list of neighbours of a vertex
    def parseNeighbours(self, x):
        return self.__dictEdges[x]

    #function that returns the list of vertices
    def parseKeys(self):
        return list(self.__dictEdges.keys())


    #function that creates lists of subgraphs containg the strongly connected components
    def __storeAsSubgraph(self, connectedComponent):
        g = UndirectedGraph(0)
        for v in connectedComponent:
            g.addVertex(v)
        for v in connectedComponent:
            for x in self.__dictEdges[v]:
                try:
                    g.addEdge(v, x)
                except undirected_exception:
                    continue
        self.__subgraphs.append(g)

    #function that finds the strongly connected components of the graph usind DFS(or depth first search/traversal)
    def connectedComponents(self):
        self.__subgraphs = []
        visited = []
        for i in range(0, len(self.__dictEdges)):
            visited.append(False)
        for i in range(0, len(self.__dictEdges)):
            if visited[i] == False:
                connectedComponent = self.dfs(i)
                self.__storeAsSubgraph(connectedComponent)
                for x in connectedComponent:
                    visited[x] = True

    #function that returns the list of vertices in the order they were visited --- DFS usual algorithm
    def dfs(self, start):
        explored = []
        stack = [start]
        visited = [start]
        while stack:
            node = stack.pop()
            explored.append(node)
            neighbours = self.parseNeighbours(node)
            for neighbour in neighbours:
                if neighbour not in visited:
                    stack.append(neighbour)
                    visited.append(neighbour)
        return explored[:]


    #function for printing subgraphs(strongly connected components)
    def printSubgraphs(self):
        for sg in self.__subgraphs:
            print(sg.parseKeys())
