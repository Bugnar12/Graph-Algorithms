from src.Domain.graph import Graph
from src.Service.directed_graph import DirectedGraph
from src.Console.main import Console
from src.Validation.validation import Validation
from src.read_file import read_graph_from_file
from src.write_file import write_graph_to_file

graph = Graph()
service = DirectedGraph(graph)
validation = Validation(graph, service)
console = Console(service, graph, validation)
console.start()
