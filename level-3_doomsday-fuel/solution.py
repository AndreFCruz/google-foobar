"""Doomsday Fuel

This problem can be reduced to finding the limiting matrix
of an Absorbing Markov Chain, given a transition matrix
between states.

1. Transform the input transition matrix M into the standard
form matrix, i.e., place all absorbing states (terminal
states) on the first lines of the transition matrix, and all
other states in the bottom;

2. Then, divide P into the following sub-matrices:

         |  I  | 0  |
    P =  |  R  | Q  | ,

where:
    - I is the identity matrix (all terminal states point
    to themselves);
    - R is the transition matrix from non-absorbing states
    to absorbing states;
    - Q is the transition matrix from non-absorbing states
    to other non-absorbing states;

3. Finally, we want to find out the limiting matrix:
    the limit of P^k as k goes to infinity;
    (this will contain the final probabilities of reaching
    the given terminal state after infinite iterations)

    The limiting matrix L is given by:

         |  I  | 0  |
    L =  | FR  | 0  | ,

    where the fundamental matrix is given by:
    
    F = (I - Q)^-1 ;

"""
from fractions import Fraction, gcd


### Utils for matrix manipulation (please give me numpy)
def mat_identity(n):
    """
    Returns an identity matrix of size n.
    """
    return [[1 if col == row else 0 for col in range(n)] for row in range(n)]

def mat_add(A, B):
    """
    Returns A - B.
    """
    n = len(A)  # assume matrices are of equal size
    return [[A[row][col] + B[row][col] for col in range(n)] for row in range(n)]

def mat_subtract(A, B):
    """
    Returns A - B.
    """
    n = len(A)  # assume matrices are of equal size
    return [[A[row][col] - B[row][col] for col in range(n)] for row in range(n)]

def mat_get_col(M, col):
    """
    Returns the column col of matrix M.
    """
    n = len(M)
    assert col < n, "Invalid column"
    return [M[row][col] for row in range(n)]

def mat_mult(A, B):
    """
    Returns AB.
    """
    return [
        [
            sum(a * b for a, b in zip(row_A, col_B))
            for col_B in zip(*B)
        ] for row_A in A
    ]

# Based on the first Google hit on how to invert a matrix in pure python;
# In practice we'd just use numpy...
def mat_invert(A):
    """Matrix inversion.
    Returns A^-1.
    """
    n = len(A)  # assume it's an invertible square matrix
    B = mat_identity(n)
    
    for diag in range(n):
        diag_scaler = Fraction(1, A[diag][diag]) if A[diag][diag] != 0 else 0
        
        # Scale diag row
        for col in range(n):
            A[diag][col] *= diag_scaler
            B[diag][col] *= diag_scaler
        
        # Scale all rows *except* diag row
        for row in range(n):
            if row == diag: continue  # skip diag row
            row_scaler = A[row][diag]

            for col in range(n):
                A[row][col] = A[row][col] - row_scaler * A[diag][col]
                B[row][col] = B[row][col] - row_scaler * B[diag][col]

    # Return inverted matrix
    return B

### ^ matrix manipulation functions ^


def solution(M):
    """
    Given a transition matrix M, this function outputs
    the probabilities of reaching the terminal states.
    [
        prob. term. state 1,
        prob. term. state 2,
        ...,
        common denominator,
    ]

    This is solved by taking M as the transition matrix
    in an absorbing Markov chain, and finding the
    limiting matrix.
    """
    terminal = [not any(transitions) for transitions in M]
    
    # Only one terminal state ?
    if sum(terminal) == 1: return [1, 1]
    
    # Pre-processing full matrix M
    P = [
        [
            1
            if terminal[from_state] and from_state == to_state  # edge from terminal state to itself
            else (Fraction(prob, sum(M[from_state])) if sum(M[from_state]) > 0 else 0)  # TODO: catch 0 ?
            for to_state, prob in enumerate(probabilities)
        ]
        for from_state, probabilities in enumerate(M)
    ]
    
    # Sub-matrix from non-absorbing states to other non-absorbing states
    Q = [
        [P[row][col] for col, is_term_inner in enumerate(terminal) if not is_term_inner]
        for row, is_term_outer in enumerate(terminal) if not is_term_outer
    ]

    # Sub-matrix from non-absorbing states to absorbing (terminal) states
    R = [
        [P[row][col] for col, is_term_inner in enumerate(terminal) if is_term_inner]
        for row, is_term_outer in enumerate(terminal) if not is_term_outer
    ]
    
    # Compute fundamental matrix F = (I - Q)^-1
    F = mat_invert(mat_subtract(mat_identity(len(Q)), Q))
    
    # Compute limiting matrix L = FR
    L = mat_mult(F, R)
    
    # Probabilities from initial state 0
    probs = L[0]
    
    # Find least common denominator
    lcm = None
    for frac in probs:
        denom = frac.denominator
        lcm = denom if lcm is None else (lcm * denom) // gcd(lcm, denom)
    
    return [
        f.numerator * lcm // f.denominator for f in probs
    ] + [lcm]


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
