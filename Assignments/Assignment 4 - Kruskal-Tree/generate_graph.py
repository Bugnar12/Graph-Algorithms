import sys

from src.Domain.graph import GraphException
from random import randint


def generate_random_graph(graph, directed_graph, number_of_vertices, number_of_edges):
    if number_of_vertices * number_of_vertices < number_of_edges:
        raise GraphException("Invalid input!")
    graph.edges = 0
    directed_graph.initialize_graph(number_of_vertices)
    while number_of_edges > 0:
        first_vertex = randint(0, len(graph.vertices) - 1)
        second_vertex = randint(0, len(graph.vertices) -1)
        try:
            cost = randint(-sys.maxsize, sys.maxsize)
            directed_graph.add_edge(first_vertex, second_vertex, cost)
            number_of_edges = number_of_edges - 1
        except:
            continue
