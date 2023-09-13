import copy
import queue
from re import search
from queue import PriorityQueue
import heapq

from src.Domain.graph import GraphException, Graph


class DirectedGraph:

    def __init__(self, graph):
        self._graph = graph
        self._inbounds = {}
        self._outbounds = {}
        self._cost = {}
        # self.initialize_vertices_in()
        # self.initialize_vertices_out()

    @property
    def inbounds(self):
        return self._inbounds

    @inbounds.setter
    def inbounds(self, key, value):
        self._inbounds[key] = value

    @property
    def outbounds(self):
        return self._outbounds

    @outbounds.setter
    def outbounds(self, key, value):
        self._outbounds[key] = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, key, value):
        self._cost[key] = value

    def copy_graph(self):
        return copy.deepcopy(self._graph), copy.deepcopy(self)

    def initialize_graph(self, number_of_vertices):
        self._inbounds.clear()
        self._outbounds.clear()
        self._cost.clear()
        self._graph.initialize_vertices(number_of_vertices)
        self.initialize_costs()
        self.initialize_vertices_in()
        self.initialize_vertices_out()

    def initialize_costs(self):
        for i in range(0, self._graph.edges):
            self._cost[i] = []

    def initialize_vertices_in(self):
        for i in range(len(self._graph.vertices)):
            self._inbounds[i] = []

    def initialize_vertices_out(self):
        for i in range(len(self._graph.vertices)):
            self._outbounds[i] = []

    def get_inbound_vertices(self, vertex):
        return self._inbounds[vertex]

    def get_outbound_vertices(self, vertex):
        return self._outbounds[vertex]

    def add_vertex(self, new_vertex):
        self._graph.add_vertex(new_vertex)
        self._inbounds[new_vertex] = []
        self._outbounds[new_vertex] = []

    def remove_vertex(self, vertex):
        self._graph.remove_vertex(vertex)
        for existent_vertex in self._inbounds:
            if vertex in self._inbounds[existent_vertex]:
                self._inbounds[existent_vertex].remove(vertex)
            elif vertex in self._outbounds[existent_vertex]:
                self._outbounds[existent_vertex].remove(vertex)
        del self._inbounds[vertex]
        del self._outbounds[vertex]

    def add_edge(self, first_vertex, second_vertex, cost):
        if self._graph.check_existence_of_vertex(first_vertex) and self._graph.check_existence_of_vertex(second_vertex):
            if second_vertex in self._outbounds[first_vertex]:
                raise GraphException('The given edge already exists!')
            else:
                self._inbounds[second_vertex].append(first_vertex)
                self._outbounds[first_vertex].append(second_vertex)
                final_key = str(first_vertex) + '-' + str(second_vertex)
                self._cost[final_key] = cost
                self._graph.edges = self._graph.edges + 1
        else:
            raise GraphException('One of the given vertices does not exist! Try again!!!')

    def delete_edge(self, first_vertex, second_vertex):
        if self._graph.check_existence_of_vertex(first_vertex) and self._graph.check_existence_of_vertex(second_vertex):
            if second_vertex not in self._outbounds[first_vertex]:
                raise GraphException('The given edge does not exists!')
            else:
                self._inbounds[second_vertex].remove(first_vertex)
                self._outbounds[first_vertex].remove(second_vertex)
                final_key = str(first_vertex) + '-' + str(second_vertex)
                del self._cost[final_key]
                self._graph.edges = self._graph.edges - 1

    def add_cost(self, first_edge, second_edge, cost):
        final_key = str(first_edge) + '-' + str(second_edge)
        self._cost[final_key] = cost

    def add_vertex_to_inbounds(self, first_vertex, second_vertex):
        self._inbounds[second_vertex].append(first_vertex)

    def add_vertex_to_outbounds(self, first_vertex, second_vertex):
        self._outbounds[first_vertex].append(second_vertex)

    def parse_outbound_vertices(self, vertex):
        vertices = self.get_outbound_vertices(vertex)
        for vertex in vertices:
            yield vertex

    def parse_inbound_vertices(self, vertex):
        vertices = self.get_inbound_vertices(vertex)
        for vertex in vertices:
            yield vertex

    def get_in_degree(self, vertex):
        inbound_vertices = self.get_inbound_vertices(vertex)
        return len(inbound_vertices)

    def get_cost(self):
        for key in self._cost.keys():
            yield key

    def get_nr_of_vertices(self):
        return self._graph.get_nr_of_vertices()

    def get_out_degree(self, vertex):
        outbound_vertices = self.get_outbound_vertices(vertex)
        return len(outbound_vertices)

    def check_existence_edge(self, first_edge, second_edge):
        outbound_vertices = self.get_outbound_vertices(first_edge)
        for vertex in outbound_vertices:
            if vertex == second_edge:
                return True
        return False

    def change_cost(self, key, cost):
        self._cost[key] = cost

    def change_cost_edge(self, first_vertex, second_vertex, cost):
        final_key = str(first_vertex) + '-' + str(second_vertex)
        keys = self.get_cost()
        for key in keys:
            if key == final_key:
                self.change_cost(key, cost)

    def get_cost_for_edge(self, first_vertex, second_vertex):
        if self.is_edge(first_vertex, second_vertex):
            final_key = str(second_vertex) + '-' + str(first_vertex)
            return self._cost[final_key]
        else:
            return float('inf')

    def is_edge(self, start_vertex, end_vertex):
        """
        Checks if there is an edge between the 2 given vertices
        :return: true if there is an edge from start_vertex to end_vertex, false otherwise
        :raises GraphException: nonexistent edge
        """
        return end_vertex in self._inbounds[start_vertex]

    def get_lowest_cost_path(self, start_vertex, end_vertex):
        """
        Finds the lowest cost path between 2 vertices
        :param start_vertex: starting vertex of path
        :param end_vertex: ending vertex of path
        """
        # call the function to get the distance and the next dictionary
        dist, next = self.backwards_Dijkstra(start_vertex, end_vertex)
        # we dont have a walk
        if dist[start_vertex] == 100000000001:
            raise GraphException("No walk!")

        # form the path from next dictionary
        path = []
        v = start_vertex
        while v != end_vertex:
            path.append(v)
            v = next[v]

        path.append(end_vertex)
        return path, dist[start_vertex]

    def backwards_Dijkstra(self, start_vertex, end_vertex=None):
        """
        Finds a lowest cost walk between the given vertices, using a "backwards" Dijkstra algorithm
        :param start_vertex: starting vertex of path
        :param end_vertex: ending vertex of path
        """
        q = PriorityQueue()
        # dictionary that holds for each vertex the cost of the minimum cost walk
        dist = {}
        for i in range(self._graph.get_nr_of_vertices()):
            dist[i] = 100000000001
        # dictionary that holds for each vertex its successor on the path
        next = {}
        # initialize the lowest cost walk to end_vertex with 0
        dist[end_vertex] = 0
        # add the tuple(stance, vertex) to the priority queue
        q.put((dist[end_vertex], end_vertex))

        visited = set()
        visited.add(end_vertex)
        while not q.empty():
            # get the last item from the queue
            distance, vertex = q.get()

            # go through the inbound neighbor of the vertex
            # check if the distance is minimum
            # if it is, add it to the path and update the distance to the vertex neighbor from the end_vertex
            for neighbor in self._inbounds[vertex]:
                cost = self.get_cost_for_edge(vertex, neighbor)
                if cost is not None and (neighbor not in visited or dist[neighbor] > dist[vertex] + cost):
                    dist[neighbor] = dist[vertex] + cost
                    visited.add(vertex)
                    q.put((dist[neighbor], neighbor))
                    next[neighbor] = vertex
        return dist, next

    def parsedIN(self):
        return self._inbounds.keys()

    def numberOfEdges(self):
        return len(self._cost)

    def minTreeKruskal(self, mintree):
        """
        Finds the minimum spanning tree of the graph using Kruskal's algorithm
        :return: the minimum spanning tree
        """
        min_cost = 0
        count = 0
        # Create a list of sets to represent the disjoint sets (trees)
        trees = [{i} for i in range(self._graph.get_nr_of_vertices())]

        # Sort the edges based on their cost
        ordered_edges = sorted(self._cost.items(), key=lambda item: item[1])

        for edge, cost in ordered_edges:
            v, w = edge.split('-')  # Split the edge string into its vertices
            v = int(v)
            w = int(w)

            set_v = None
            set_w = None

            # Find the sets (trees) to which v and w belong
            for tree in trees:
                if v in tree:
                    set_v = tree
                if w in tree:
                    set_w = tree

            # If v and w belong to different sets, add the edge to the minimum spanning tree
            if set_v != set_w and (w, v) not in mintree:
                min_cost += cost
                count += 1
                mintree.append((v, w))

                # Merge the sets (trees) by combining set_v and set_w
                set_v.update(set_w)
                trees.remove(set_w)

            # If we have included all vertices in the minimum spanning tree, exit the loop
            if count == self._graph.get_nr_of_vertices() - 1:
                break

        return min_cost

    # def check_for_isolated_vertex(self, vertex):
    #     first_found = False
    #     second_found = False
    #     for key in self._inbounds.keys():
    #         if vertex == key:
    #             first_found = True
    #
    #     for key in self._outbounds.keys():
    #         if vertex == key:
    #             second_found = True
    #
    #     if first_found and second_found:
    #         return True
    #     elif first_found and not second_found:
    #         return True
    #     elif not first_found and second_found:
    #         return True
    #     else:
    #         return False

    # def remove_vertex(self, vertex):
    #     self._graph.remove_vertex(vertex)
    #
    #     for to_find_vertex in self._inbounds:
    #         if to_find_vertex == vertex:
    #             self._inbounds[to_find_vertex].remove(vertex)
    #
    #     del self._outbounds[vertex]
    #
    # def remove_edges_with_cost(self, vertex):
    #     string_vertex = str(vertex)
    #     for key in self._cost.keys():
    #         if search(string_vertex, key):
    #             del self._cost[key]