from src.create_file import create_text_file


def write_graph_to_file2(file_name, graph, service):

    create_text_file(file_name)

    try:
        file = open(file_name, 'wt')
        vertex_edges = str(len(graph.vertices)) + ' ' + str(graph.edges)
        file.write(vertex_edges)
        file.write('\n')
        for first_vertex in service.outbounds:
            vertices = service.get_outbound_vertices(first_vertex)
            second_vertices = service.get_inbound_vertices(first_vertex)
            if len(vertices) == 0 and len(second_vertices) == 0:
                file.write(str(first_vertex))
                file.write('\n')
            else:
                for second_vertex in vertices:
                    final_key = str(first_vertex) + '-' + str(second_vertex)
                    params = str(first_vertex) + ' ' + str(second_vertex) + ' ' + str(service.cost[final_key])
                    file.write(params)
                    file.write('\n')
        file.close()
    except Exception as e:
        print(e)