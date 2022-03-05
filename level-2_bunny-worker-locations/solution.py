# Bottom row: sum of first n natural numbers
# > solution(x, 1) := x * (x+1) / 2

def solution(x, y):
    # Get index of diagonal (point at y=1 that belongs to the same diagonal)
    diagonal_idx = x + y - 1

    # ID of point at (1, diagonal_idx)
    sum_natural_nums = diagonal_idx * (diagonal_idx + 1) / 2

    # ID of point at (x, y) will be (sum_natural_nums - (diagonal_idx - x))
    return str(sum_natural_nums - (diagonal_idx - x))   # Return must be type string

if __name__ == '__main__':
    print(solution(3, 2))
    # Output: 9

    print(solution(5, 10))
    # Output: 96
