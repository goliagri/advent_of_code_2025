#https://adventofcode.com/2025/day/11
INPUT_FILENAME = "inputs/input_11.txt"


def count_paths(graph: dict, source = 'you', sink = 'out'):
    #Assume graph is DAG
    # idea: search through algo, but always pause on node until all incomming edges have been traversed, counting path total, then proceed.

    num_incomming_edges = {}
    num_seen_incomming_edges = {}
    num_acc_paths = {source:1, sink:0}
    for dest_nodes in graph.values():
        for node in dest_nodes:
            if not node in num_incomming_edges.keys():
                num_incomming_edges[node] = 0
                num_seen_incomming_edges[node] = 0
                num_acc_paths[node] = 0
            num_incomming_edges[node] += 1

    #prune dead starts to make edge counting actually correct
    while True:
        to_prune = [a for a in graph.keys() if num_incomming_edges.setdefault(a, 0) == 0]
        if not to_prune:
            break
        for a in to_prune:
            num_incomming_edges[a] = -1
            if a == source:
                continue
            for b in graph[a]:
                num_incomming_edges[b] -= 1

    frontier = [source]
    while frontier:
        cur = frontier.pop(0) #bfs
        cur_path_count = num_acc_paths[cur]
        succs = graph.setdefault(cur, []) 

        for next_node in succs: 
            num_seen_incomming_edges[next_node] += 1
            num_acc_paths[next_node] += cur_path_count
            if num_seen_incomming_edges[next_node] == num_incomming_edges[next_node]:
                frontier.append(next_node)

    return num_acc_paths[sink]

def count_paths_traversing_nodes(graph: dict, must_traverse, source = 'svr', sink = 'out'):
    #same as above but must traverse all nodes in must_traverse to be a valid path
    #idea: just count paths based on # of must_traverse traversed (since no loops), so num_acc_paths is now a dict of lists of ints
    num_incomming_edges = {}
    num_seen_incomming_edges = {}
    num_acc_paths = {source:[1] + [0 for _ in must_traverse], sink:[0 for _ in range(len(must_traverse)+1)]}
    for dest_nodes in graph.values():
        for node in dest_nodes:
            if not node in num_incomming_edges.keys():
                num_incomming_edges[node] = 0
                num_seen_incomming_edges[node] = 0
                num_acc_paths[node] = [0 for _ in range(len(must_traverse)+1)]
            num_incomming_edges[node] += 1

    #prune dead starts to make edge counting actually correct
    while True:
        to_prune = [a for a in graph.keys() if num_incomming_edges.setdefault(a, 0) == 0]
        if not to_prune:
            break
        for a in to_prune:
            num_incomming_edges[a] = -1
            if a == source:
                continue
            for b in graph[a]:
                num_incomming_edges[b] -= 1

    frontier = [source]
    while frontier:
        cur = frontier.pop(0) #bfs
        cur_path_count_list = num_acc_paths[cur]
        succs = graph.setdefault(cur, []) 

        if cur in must_traverse:
            cur_path_count_list = [0] + cur_path_count_list[:-1] #slide it over 1 to the right

        for next_node in succs: 
            num_seen_incomming_edges[next_node] += 1
            num_acc_paths[next_node] = [sum(a) for a in zip(cur_path_count_list, num_acc_paths[next_node])]
            if num_seen_incomming_edges[next_node] == num_incomming_edges[next_node]:
                frontier.append(next_node)

    return num_acc_paths[sink][-1]

def make_graph(data):
    edges = {}
    for edge in data:
        n1 = edge[0][0]
        dests = edge[1]
        if not n1 in edges:
            edges[n1] = []
        edges[n1].extend(dests)
    
    edges['out'] = []

    return edges

def make_reverse_graph(data):
    edges = {}
    for edge in data:
        n1 = edge[0][0]
        dests = edge[1]
        for n2 in dests:
            if not n2 in edges:
                edges[n2] = []
            edges[n2].append(n1)
    
    edges['you'] = []

    return edges


def get_data():
    with open(INPUT_FILENAME) as f:
        lines = f.readlines()
    data = [[a.strip().split(' ') for a in line.split(':')] for line in lines]
    return data

def main():
    data = get_data()
    reverse_graph = make_reverse_graph(data)
    graph = make_graph(data)
    p1_sol = count_paths(reverse_graph, 'out', 'you')

    p2_sol = count_paths_traversing_nodes(graph, ['dac', 'fft'])

    print('number of unique paths from you to out {}'.format(p1_sol))
    print('num of unique paths svr to out through dac and fft: {}'.format(p2_sol))


if __name__ == '__main__':
    main()