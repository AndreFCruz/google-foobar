import heapq

def translate_columns(columns):
    """
    Translate the given incidence matrix columns into the actual response.
    For example, considering the given example of `solution(5, 3)`, we would get
    the following incidence matrix:

    1111110000
    1110001110
    1001101101
    0101011011
    0010110111

    which corresponds to the columns:
    [
        [1, 1, 1, 0, 0],
        [1, 1, 0, 1, 0],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 1, 0],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 0, 1],
        [0, 1, 0, 1, 1],
        [0, 0, 1, 1, 1],
    ]

    which corresponds to the solution:
    [0, 1, 2, 3, 4, 5],
    [0, 1, 2, 6, 7, 8],
    [0, 3, 4, 6, 7, 9],
    [1, 3, 5, 6, 8, 9],
    [2, 4, 5, 7, 8, 9]

    The goal in this method is to convert the columns into the solution.
    """
    res = []

    for _ in range(len(columns[0])):
        res.append([])

    for i in range(len(columns[0])):
        for j in range(len(columns)):
            if columns[j][i]:
                res[i].append(j)

    return res

def compute_IM_columns(v, k):
    """Compute the columns of the incidence matrix with the given parameters"""

    columns = []
    # As priority for our heap we are first using the number of 1s and
    # then the idx. We use the negative on both values because the heap is
    # ordered in ascending manner and we want the highest number of ones with
    # highest idx to be processed first
    stack = [(0, 0, [0] * v)]

    while stack:
        negative_sum_ones, negative_idx, current = heapq.heappop(stack)
        idx = -negative_idx
        sum_ones = -negative_sum_ones

        # Skip if it is not possible to get k 1s from the current idx
        if idx > (v - k + sum_ones):
            continue

        # We are just copying the list but doing it in a python2 friendly way
        current_1 = current[:]
        current_1[idx] = 1

        if sum_ones + 1 == k:
            columns.append(current_1)
        else:
            heapq.heappush(stack, (negative_sum_ones - 1, -(idx + 1), current_1))

        heapq.heappush(stack, (negative_sum_ones, -(idx + 1), current[:]))

    return columns


def solution(num_buns, num_required):
    """
    This solution is inspired in the principles of Block design (Combinatorics)
    https://en.wikipedia.org/wiki/Block_design

    However, in this case, there is not the need for us to compute sigma, r or
    b, as we don't need these parameters to compute the incidence matrix. Having
    the incidence matrix we can then compute the blocks (the actual problem
    solution)
    """
    v = num_buns
    # If only 1 bunny worker is required, that means that all bunny workers will
    # have to have this key, hence, this means that k = v.
    #
    # On the other hand, if all bunny workers are required (num_buns ==
    # num_required), then k must be 1, meaning that only 1 bunny worked will
    # have a given key.
    k = v + 1 - num_required

    return translate_columns(compute_IM_columns(v, k))


if __name__ == "__main__":
    assert solution(2, 1) == [[0], [0]]
    assert solution(4, 4) == [[0], [1], [2], [3]]
    assert solution(3, 2) == [[0, 1], [0, 2], [1, 2]]
    assert solution(5, 3) == [
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 6, 7, 8],
        [0, 3, 4, 6, 7, 9],
        [1, 3, 5, 6, 8, 9],
        [2, 4, 5, 7, 8, 9]
    ]
    print("All tests passed")