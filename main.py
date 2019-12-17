import math


def read_graph():
    file_in = open("file_in.txt", 'r')
    line_for_nums = file_in.readline().split()
    num_of_x = int(line_for_nums[0])
    num_of_y = int(line_for_nums[1])
    graph_matrix_for_x = [None] * num_of_x
    for x in range(num_of_x):
        graph_matrix_for_x[x] = [None] * num_of_x
    for x in range(num_of_x):
        line = file_in.readline().split()
        for vertex in line:
            graph_matrix_for_x[x][int(vertex) - 1] = 1
    graph_matrix_for_y = [None] * num_of_y
    for y in range(num_of_y):
        graph_matrix_for_y[y] = [None] * num_of_y
    for y in range(num_of_y):
        line = file_in.readline().split()
        for vertex in line:
            graph_matrix_for_y[y][int(vertex) - 1] = 1
        # print(pairs)
    file_in.close()
    return graph_matrix_for_x, graph_matrix_for_y


def make_net_from_sets(matr_for_x, matr_for_y):
    num_of_x = len(matr_for_x)
    num_of_y = len(matr_for_y)
    n = num_of_x + num_of_y + 2
    net_matr = [None]*n
    print(n)
    for i in range(n):
        net_matr[i] = [None]*n
    start = 0
    end = n - 1
    for x in range(num_of_x):
        net_matr[start][x+1] = 1
    for y in range(num_of_y):
        net_matr[num_of_x + y + 1][end] = 1
    for x_vertex in range(num_of_x):
        for y_vertex in range(num_of_y):
            net_matr[x_vertex + 1][y_vertex + 1] = matr_for_x[x_vertex][y_vertex]
    for y_array in range(num_of_y):
        for x_vertex in range(num_of_x):
            net_matr[x_vertex + 1][y_array + 1] = matr_for_y[y_array][x_vertex]
    return net_matr

#do with ribs better!


matr_for_x, matr_for_y = read_graph()
print(make_net_from_sets(matr_for_x, matr_for_y))


def labeling(net_matr, flow_matr, start, end):
    n = len(net_matr)
    choice = [None] * n
    previous = [None] * n
    labeled_vertices_queue = []
    label_of_vertices = [math.inf] * n
    labeled_vertices_queue.append(start)
    while label_of_vertices[end] is math.inf and len(labeled_vertices_queue) != 0:
        temp_vertex = labeled_vertices_queue.pop(0)
        for vertex in range(n):
            if label_of_vertices[vertex] is math.inf and net_matr[temp_vertex][vertex] - flow_matr[temp_vertex][vertex] > 0:
                label_of_vertices[vertex] = min(label_of_vertices[temp_vertex],
                                                net_matr[temp_vertex][vertex] - flow_matr[temp_vertex][vertex])
                previous[vertex] = temp_vertex
                labeled_vertices_queue.append(vertex)
                choice[vertex] = 1
            for local_vertex in range(n):
                if local_vertex != start:
                    if label_of_vertices[local_vertex] is math.inf and flow_matr[temp_vertex][local_vertex] > 0:
                        label_of_vertices[local_vertex] = min(label_of_vertices[temp_vertex], flow_matr[temp_vertex][local_vertex])
                        previous[local_vertex] = temp_vertex
    return label_of_vertices, previous, choice


def ford_fulkerson(net_matr, start, end):
    n = len(net_matr)
    flow_matr = [None] * n
    max_flow_value = 0
    for i in range(n):
        flow_matr[i] = [None] * n
    for vertex in range(n):
        for local_vertex in range(n):
            flow_matr[vertex][local_vertex] = 0
        max_flow_value = 0
        while label_of_vertices[end] is not math.inf:
            label_of_vertices, previous, choice = labeling(net_matr, flow_matr, start, end)
            if label_of_vertices[end] < math.inf:
                max_flow_value = max_flow_value + label_of_vertices[end]
                vertex = end
                while vertex != start:
                    local_vertex = previous[vertex]
                    if choice[vertex] == 1:
                        flow_matr[local_vertex][vertex] += label_of_vertices[end]
                    else:
                        flow_matr[vertex][local_vertex] -= label_of_vertices[end]
                    vertex = local_vertex
    return max_flow_value, flow_matr


print(read_graph())



