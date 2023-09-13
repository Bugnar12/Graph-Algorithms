from src.create_file import create_text_file


def write_graph_to_file(file_name, graph, service):

    create_text_file(file_name)

    try:
        file = open(file_name, 'wt')
        vertex_edges = str(len(graph.vertices)) + ' ' + str(graph.edges)
        file.write(vertex_edges)
        file.write('\n')
        for first_vertex in service.outbounds:
            vertices = service.get_outbound_vertices(first_vertex)
            for second_vertex in vertices:
                final_key = str(first_vertex) + '-' + str(second_vertex)
                params = str(first_vertex) + ' ' + str(second_vertex) + ' ' + str(service.cost[final_key])
                file.write(params)
                file.write('\n')
        file.close()
    except Exception as e:
        print(e)