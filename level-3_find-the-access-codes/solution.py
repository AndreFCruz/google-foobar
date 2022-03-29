def solution(l):
    # Since we must also be able to deal with repeated values in l,
    # our 'doubles' dict will be in the format 'num: [(idx in l, count)]'
    doubles = dict()
    triples = 0

    # Populate doubles with all values in the format 'num: [(idx in l, 0)]'
    # performance O(n)
    for i in range(len(l)):
        if l[i] in doubles:
            doubles[l[i]][i] = 0
        else:
            doubles[l[i]] = {i: 0}

    # Compute the doubles and triples - performance O(n^2)
    # Initially I had this as two separate O(n^2) loops: one for the doubles
    # another for the triples. However, since the computation of a triple always
    # uses only doubles of inferior idx, we can then merge into a single set of
    # nested loops:
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if not l[j] % l[i]:
                # This is yet another double of type (l[i], l[j])
                doubles[l[j]][j] += 1
                # Since this is a possible triple, then consider all triples
                # that use the doubles that take i as the 2nd element
                triples += doubles[l[i]][i]

    return triples


if __name__ == "__main__":
    assert solution([1, 2, 3, 4, 5, 6]) == 3
    assert solution([1, 1, 1]) == 1

    print("All tests passed")
