
def solution(M, F):
    """
    Each bomb can generate one of the other type of bomb, so
    they're **interchangeable**.

    Start from the end-point (number of bombs required), and
    work backwards until reaching the starting point of (1, 1).

    Find the bomb with largest gap between target and current
    (M > F ? M : F), and produce (remove from target, working
    backwords).
    """
    M, F = int(M), int(F)

    # Bomb types are interchangeable
    if M < F:
        M, F = F, M

    # Use M for the largest number and always decrement M in
    # each iteration;
    # If M is no longer the largest number, switch M,F;

    cnt = 0
    while M != F:
        # Replicate F bombs cnt number of times,
        # to produce cnt*F bombs of type M;
        cnt += M // F
        M = M % F
        if M < F:
            M, F = F, M
        
        if M <= 0 or F <= 0:
            break

    return str(cnt-1) if M == 1 else "impossible"


if __name__ == "__main__":
    print(solution("4", "7"))
    # Output: 4

    print(solution("2", "1"))
    # Output: 1

    print(solution("2", "4"))
    # Output: impossible
