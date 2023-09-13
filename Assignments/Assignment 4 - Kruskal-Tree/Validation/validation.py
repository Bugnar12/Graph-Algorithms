from src.Domain.graph import GraphException


class Validation:

    def __init__(self, graph, service):
        self._graph = graph
        self._service = service

    def exist_vertex(self, first_vertex, second_vertex):
        if self._graph.find_vertex(first_vertex) is False:
            raise GraphException("The first given vertex doesn't exist!")
        if self._graph.find_vertex(second_vertex) is False:
            raise GraphException("The second vertex doesn't exist!")

