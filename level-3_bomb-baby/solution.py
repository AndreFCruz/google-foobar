
def solution(M, F):
    M, F = int(M), int(F)

    if M < F:
        M, F = F, M

    cnt = 0
    while M != F:
        cnt += M // F
        M = M % F
        if M < F:
            M, F = F, M
        
        if min(M, F) <= 0:
            break

    return str(cnt-1) if M == 1 else "impossible"


if __name__ == "__main__":
    print(solution("4", "7"))
    # Output: 4

    print(solution("2", "1"))
    # Output: 1

    print(solution("2", "4"))
    # Output: impossible
