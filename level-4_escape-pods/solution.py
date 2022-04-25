"""
This is a standard max flow problem.

1. Join all sources with a single artificial source node parent;
2. Join all sinks with a single artificial sink node child;
3. Run a max flow algorithm (e.g., Ford-Fulkerson);
"""
from queue import Queue
INF_FLOW = float("+inf")

class Node:
    def __init__(self, id, edges: dict[int, int]):
        self.id = id
        self.edges = edges  # Dictionary of (destination_node_id -> edge_capacity)
    
    def subtract_edge_capacity(self, dest, value):
        assert dest in self.edges
        assert self.edges[dest] >= value

        self.edges[dest] -= value
        if self.edges[dest] == 0:
            self.edges.pop(dest)

def find_path_dfs(src, dst, all_nodes) -> tuple[list[str], int]:
    """Runs DFS to find a path from source to destination.
    
    Returns a tuple: (path, max_flow)
    - path: the ordered list of node ids;
    - max_flow: the maximum flow that passes through this path
    (i.e., the edge with lowest capacity);

    We would need a "visited" array in case of loops.
    """
    src_node = all_nodes[src]
    src_edges = src_node.edges

    for edge, edge_capacity in src_edges.items():
        # Base case
        if edge == dst: # Found a path
            return [dst], edge_capacity

        # Recursive case
        ret = find_path_dfs(edge, dst, all_nodes)
        if ret is None: # No path found via edge
            continue
        else:           # Path found!
            path, path_flow = ret
            return [edge] + path, min(edge_capacity, path_flow)
    
    return None # No path to dst node

def ford_fulkerson_max_flow(src, dst, all_nodes: dict):
    """Runs the Ford-Fulkerson max flow algorithm.

    1. Find a path from source to sink, with all edges carrying
    positive flow, p;
    2. Subtract p from all edges of that path, and add p to the
    total flow;
    3. Repeat until there are no more paths from source to sink;
    """
    total_flow = 0

    while True:
        # Find path from source to destination
        ret = find_path_dfs(src, dst, all_nodes)
        if ret is None: # No more paths found
            return total_flow

        # Unpack result
        path, path_flow = ret

        # Subtract flow to current graph
        curr_node = src
        for edge_node in path:
            all_nodes[curr_node].subtract_edge_capacity(edge_node, path_flow)
            curr_node = edge_node

        # Add this path's flow to the total flow
        total_flow += path_flow
    
    return total_flow   # This is never actually reached

def solution(entrances, exits, path):
    """
    Parse input into a graph structure, and run the Ford-Fulkerson
    max flow algorithm.
    """
    # Build graph structure
    source = Node(id="source", edges={str(e): INF_FLOW for e in entrances})
    sink = Node(id="sink", edges={})

    all_nodes: dict[str, Node] = {
        source.id: source,
        sink.id: sink,
    }

    for src, src_paths in enumerate(path):
        node_id = str(src)
        node_edges = {str(dest): flow for dest, flow in enumerate(src_paths) if flow > 0}
        all_nodes[node_id] = Node(id=node_id, edges=node_edges)

    # Build edge from exit nodes to new artificial sink
    for exit_node in exits:
        node_id = str(exit_node)
        all_nodes[node_id].edges = {"sink": INF_FLOW}

    return ford_fulkerson_max_flow(source.id, sink.id, all_nodes)

if __name__ == "__main__":
    entrances = [0, 1]
    exits = [4, 5]
    path = [
        [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
        [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
        [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
        [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
        [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
        [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
    ]

    assert solution(entrances, exits, path) == 16
