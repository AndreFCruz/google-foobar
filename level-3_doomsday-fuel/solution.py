from fractions import Fraction

def solution(m):

    node_to_child = {i: {} for i in range(len(m))}
    node_to_parent = {i: {} for i in range(len(m))}

    # Build inverse graph
    for node, edges in enumerate(m):
        sum_edges = sum(edges)

        for child, numerator in enumerate(edges):
            if numerator == 0: continue

            proba = Fraction(numerator, sum_edges)
            node_to_child[node][child] = proba
            node_to_parent[child][node] = proba

    nodes_to_explore = [0]   # stack
    # Depth-first search
    while len(nodes_to_explore) > 0:
        # TODO
        pass


if __name__ == '__main__':
    m = [
        [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
        [0,0,0,0,0,0],  # s3 is terminal
        [0,0,0,0,0,0],  # s4 is terminal
        [0,0,0,0,0,0],  # s5 is terminal
    ]

    solution(m)
