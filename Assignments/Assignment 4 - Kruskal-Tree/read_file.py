from src.Domain.graph import GraphException
from src.create_file import create_text_file

def read_graph_from_file(file_name, graph, service):

    create_text_file(file_name)

    try:
        file = open(file_name, 'rt')
        lines = file.readlines()
        first_line = False
        for line in lines:
            line = line.strip('\n')
            if first_line is False:
                graph_parameters = line.split(' ')
                if int(graph_parameters[0]) * int(graph_parameters[0]) < int(graph_parameters[1]):
                    raise GraphException("Invalid input!")
                else:
                    service.initialize_graph(int(graph_parameters[0]))
                    # graph.initialize_vertices(int(graph_parameters[0]))
                    graph.initialize_edges(int(graph_parameters[1]))
                    service.initialize_vertices_in()
                    service.initialize_vertices_out()
                    first_line = True
            elif line == '':
                continue
            else:
                graph_parameters = line.split(' ')
                service.add_vertex_to_inbounds(int(graph_parameters[0]), int(graph_parameters[1]))
                service.add_vertex_to_outbounds(int(graph_parameters[0]), int(graph_parameters[1]))
                service.add_cost(int(graph_parameters[0]), int(graph_parameters[1]), int(graph_parameters[2]))
    except Exception as e:
        pass
