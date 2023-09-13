


class GraphException(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return str(self._msg)


class Graph:

    def __init__(self):
        self._vertices = []
        self._edges = 0

    def initialize_vertices(self, number_of_vertices):
        if(len(self._vertices)) != 0:
            self._vertices.clear()
        for index in range(0, number_of_vertices):
            self._vertices.append(index)

    def initialize_edges(self, number_of_edges):
        self._edges = number_of_edges

    # def reinitialize_vertices(self):
    #     for vertex in self._vertices:
    #         self._vertices.remove(vertex)

    def add_vertex(self, new_vertex):
        if new_vertex not in self._vertices:
            self._vertices.append(new_vertex)
        else:
            raise GraphException('The given vertex already exists!!!')

    def remove_vertex(self, vertex):
        if self.check_existence_of_vertex(vertex):
            self._vertices.remove(vertex)
        else:
            raise GraphException('The given vertex does not exist!!!')

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, new_value):
        self._edges = new_value

    @property
    def vertices(self):
        return self._vertices

    def parse_vertices(self):
        for vertex in self._vertices:
            yield vertex

    def check_existence_of_vertex(self, check_vertex):
        vertices = self.parse_vertices()
        for vertex in vertices:
            if vertex == check_vertex:
                return True
        return False

    def __len__(self):
        return len(self._vertices)

    def get_nr_of_vertices(self):
        return len(self._vertices)

    def find_vertex(self, vertex):
        if vertex in self._vertices:
            return True
        return False


"""


    def add_vertices(self, vertex):
        if vertex not in self._vertices:
            self._vertices.append(vertex)
        else:
            raise GraphException("There is already an existing vertex with that value!")

    def remove_vertices(self, vertex):
        if vertex in self._vertices:
            self._vertices.remove(vertex)
        else:
            raise GraphException("The given vertex doesn't exists!")

"""
