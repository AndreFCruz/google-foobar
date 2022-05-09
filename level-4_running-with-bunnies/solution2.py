import heapq
import itertools

def floid_warshal(graph):
    # Our initial minimal distance matrix are the direct edges themselves
    dist = []
    for node in graph:
        # Python 2 friendly way of copying the 
        dist.append(node[:])

    # The flow warshal algorithm, performance O(N^3), textbook stuff
    nodes_iter = range(len(graph))
    for k in nodes_iter:
        for i in nodes_iter:
            for j in nodes_iter:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

    return dist

def has_negative_cycle(dist):
    """
    Given the distance matrix computed by the floid warshal algorithm, verify if
    we have negative cycles.
    """
    for i in range(len(dist)):
        if dist[i][i] < 0:
            return True
    return False

def get_all_paths(path):
    """
    Get all possible subpaths, as well as permutations, we can compute with the
    given path. Notice, that all paths must start and finish in the same nodes
    as of the original path.

    For example, if we are given [0, 1, 2, 3], we will return the heap:
    [(-4, [0, 1, 2, 3]), (-4, [0, 2, 1, 3]), (-3, [0, 1, 3]), (-3, [0, 2, 3]),
    (-2, [0, 3])]
    """
    stack = [path]
    res = []

    if len(path) < 2:
        raise RuntimeError("The path has to have at least a start and an end node") 

    while stack:
        curr_path = heapq.heappop(stack)

        # In case we have already processed this path in another iteration, we
        # don't need to get all of the sub paths for this path, as that has
        # already been computed / is in the stack to be computed.
        if (-len(curr_path), curr_path) in res:
            continue

        # We need to append all of the possible permutations with this path
        # Notice that we only wish to permute the middle nodes, as the start and
        # end are fixed
        for permutation_path in itertools.permutations(curr_path[1:-1]):
            heapq.heappush(
                res,
                # we add '-len(path)' as the tuple first item because of the ascending
                # sorting order. We want first the solutions that have the lengthiest
                # paths (i.e., that save the most bunnies), and then, on those with the
                # same length, we want the ones with the smaller indexes first.
                (-len(permutation_path) - 2, [curr_path[0]] + list(permutation_path) + [curr_path[-1]])
            )

        # These are the base cases for the recursion, either empty paths or
        # paths of one element (not considering start and end nodes)
        if len(curr_path) <= 2:
            continue

        # Get all subpaths without one of the elements (disconsider start and
        # end nodes)
        for i in range(1, len(curr_path) - 1):
            heapq.heappush(stack, [el for el in curr_path if el != curr_path[i]])

    return res

def verify_path(path, dist, times_limit):
    """
    This method verifies if the given path is a possible solution to the
    problem. To do so, it uses the given distance matrix computed by the floid
    warshall algorithm, as well as the input times limit. Returns true if the
    path is a solution, false otherwise
    """
    total = 0
    for i in range(0, len(path) - 1):
        total += dist[path[i]][path[i+1]]

    return total <= times_limit


def path_output_format(path):
    """
    Helper method that takes the given path and returns it in the desired
    problem output format.
    """
    res = []
    for i in range(1, len(path) - 1):
        res.append(path[i] - 1)
    return res


def solution(times, times_limit):
    # Using the floid warshall algorithm we compute, for every node, the
    # smallest distance with which we can reach any other node
    dist = floid_warshal(times)
    all_nodes_path = list(range(len(times)))
    # Using the distance matrix we verify the existence of negative cycles. If a
    # negative cycle is present then we are able to save all of the bunnies,
    # since we can use the negative cycle to create 'an infinite time buffer',
    # by running the cycle infinite times. 
    if has_negative_cycle(dist):
        return path_output_format(all_nodes_path)

    # Since we didn't find any negative cycle we will attempt a brute force
    # solution where we test all possible paths. This is only feasible since we
    # know we will have at maximum 5 bunnies to save.
    paths = get_all_paths(all_nodes_path)
    while paths:
        _, path = heapq.heappop(paths)
        if verify_path(path, dist, times_limit):
            return path_output_format(path)

    return []


if __name__ == "__main__":
    assert solution(
        [
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]
        ],
        3
    ) == [0, 1]
    assert solution(
        [
            [0, 2, 2, 2, -1],
            [9, 0, 2, 2, -1],
            [9, 3, 0, 2, -1],
            [9, 3, 2, 0, -1],
            [9, 3, 2, 2, 0]
        ],
        1
    ) == [1, 2]
    ### Self-made corner-case
    assert solution(
        [
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]
        ],
        1
    ) == []
    ###
    print("All tests passed")
