"""
Find a path spanning the highest number of nodes;
- edges may have negative weights;
- graph is directed; A->B != B->A;
- and there may be cycles;
- number of nodes is at most n=5 (plus source and destination nodes);

Method:
1. Run Bellman-Ford shortest path for each node;
  > Get matrix of shortest distances between all nodes;
  > NOTE: we can just run the Floyd-Warshall algorithm, but we need to detect negative weight cycles beforehand;
2. Enumerate all paths between the n bunnies; (brute-force approach for now...)
  > Find the path that reaches the most bunnies and has weight within the allowed time;
  > (need to update allowed time with the first and last edge - to the 1st bunny and to the door);
"""

INF = float("inf")


def bellman_ford_algorithm(matrix, src):
    """Bellman-Ford shortest path algorithm.
    Compatible w/ negative edges and will detect negative-weight cycles.

    Parameters
    ----------
    matrix : List[List[int]]
        Adjacency matrix representation of the distances between graph nodes.
    src : int
        Index of source node.

    Returns
    -------
    List[int]
        Shortest distances from source node to each other node.
    """
    num_nodes = len(matrix)

    # Initialize graph
    distances = [matrix[src][dst] for dst in range(num_nodes)]     # distances from the source to each node
    # predecessor = [src for n in range(num_nodes)]     # NOTE: don't need predecessor information for this problem

    # Relax edges repeatedly
    for _ in range(num_nodes - 1):
        for node, node_to_dest in enumerate(matrix):
            for dest in range(num_nodes):
                node_to_dest_distance = distances[node] + node_to_dest[dest]
                if node_to_dest_distance < distances[dest]:
                    distances[dest] = node_to_dest_distance
                    # predecessor[dest] = node
    
    # Check for negative-weight cycles
    for node, node_to_dest in enumerate(matrix):
        for dest in range(num_nodes):
            if distances[node] + node_to_dest[dest] < distances[dest]:
                # Found negative-weight cycle
                raise ValueError("Graph contains a negative-weight cycle. Free all the bunnies!")
    
    return distances


def subsets(set_of_elements):
    """Generate all subsets of the given set of elements.
    Number of subsets: 2^|input| - 1.
    """
    num_elems = len(set_of_elements)

    # Base case
    if num_elems == 0: return [set()]
    elif num_elems == 1: return [set_of_elements]

    # Recursive case
    all_subsets = [set_of_elements]
    for elem in set_of_elements:
        # All sets without elem
        subsets_without_elem = subsets(set_of_elements - {elem})
        all_subsets.extend(subsets_without_elem)
    
    return all_subsets


def solution(times, times_limit):
    total_nodes = len(times)
    num_bunnies = total_nodes - 2
    if num_bunnies == 0:
        return []
    elif num_bunnies < 0:
        raise ValueError("Invalid input.")

    try:
        distances = [bellman_ford_algorithm(times, node) for node in range(len(times))]
    except ValueError as err:
        # Negative-weight cycle - release all the bunnies
        return [n for n in range(len(times) - 2)]

    # Enumerate all paths between the bunnies, starting with paths that pass through all nodes
    # Return the first path that fulfills the time limit
    nodes_with_bunnies = {n for n in range(total_nodes)} - {0} - {total_nodes-1}
    print(subsets(nodes_with_bunnies))
    # for subst in subsets(nodes_with_bunnies):
    #     print(subst)



if __name__ == "__main__":
    assert solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1) == [1, 2]
    assert solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3) == [0, 1]
