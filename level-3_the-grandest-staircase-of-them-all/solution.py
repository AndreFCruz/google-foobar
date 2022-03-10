def solution(n):
    """
    Some manually made cases to understand the patterns
     3: 21
     4: 31
     5: 41, 32
     6: 51, 42; 321
     7: 61, 52, 43; 421
     8: 71, 62, 53; 521, 431
     9: 81, 72, 53, 54; 621, 531, 432
    10: 91, 82, 73, 64; 721, 631, 532, 541; 4321

    Now, lets take here an example: if we group the possible staircases with 10
    bricks we have:
        - 2-steps: 91, 82, 73, 64
        - 3-steps: 721, 631, 532, 541
        - 4-steps: 4321
    If you look at the 3-steps staircases, there are 2 that start with 5.
    Curiosly enough, the remaining steps on those 2 staircases match the
    possible staircases when we have 5 bricks. So, assuming we have used 5
    bricks for the first step, the remaining steps can be given by `5 +
    solution(10-5)`, aka, `5 + solution(5)`.
    
    But will all solutions from the subproblem always be used? Lets look at a
    4321: if we use the previous assumption we get that `solution(10)` includes
    `4 + solution(10-4)` => `4 + solution(6)` => `4 + [51, 42, 321]`. However,
    from this we can only take `321` since it is the only staircase that starts
    with a degree that is smaller than 5.
    
    From this information, I could construct the following dp solution:
    """

    # Our auxiliary dp matrix consists of a list of size n
    # 
    # For each entry, we have another list, where each entry j stores the number
    # of staircases we can make where the first step is of size j. The second
    # list is what will allow us to address the previous scenario we analysed of
    # 4321
    dp = []
    for i in range(n + 1):
        step_counters = [0] * (n + 1)
        # We are setting the diagonal as 1 as this represent staircases with a
        # single step (all bricks stacked)
        # This represents the base cases of our problem
        step_counters[i] = 1
        dp.append(step_counters)
    # When we have 0 bricks, we can't make any staircase
    dp[0][0] = 0

    # We start at 1 because we can't make staircases with 0 bricks
    for i in range(1, n + 1):
        # We start at 1 because it is impossible to make staircases where the
        # first step has 0 bricks
        for j in range(1, i + 1):
            # The staircases with i bricks that start with a step of j bricks are
            # the ones that can be built with i-j bricks and whose starting step
            # is smaller then j
            dp[i][j] += sum(dp[i-j][k] for k in range(j))

    # Remove the staircase where we have a single step (all n bricks stacked)
    return sum(dp[n]) - 1

if __name__ == "__main__":
    assert solution(3) == 1
    # Self made usecases
    assert solution(4) == 1
    assert solution(5) == 2
    assert solution(10) == 9
    # Self made usecases end
    assert solution(200) == 487067745
    print("All tests passed")