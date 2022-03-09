def numberToBase(n, b, l):
    if n == 0:
        return "".join(["0"] * l)
    digits = ""
    while n:
        digits += str(int(n % b))
        n //= b

    # l controls the string length
    filler_list = ["0"] * (l - len(digits))
    return "".join(filler_list) + digits[::-1]

def solution(n, b):
    found_nums = []
    num = n

    while num not in found_nums:
        found_nums.append(num)

        # Computing x and y
        x = int("".join(sorted(num, reverse=True)), b)
        y = int("".join(sorted(num)), b)
        # Computing new n
        num = numberToBase(x-y, b, len(n))

    return len(found_nums) - found_nums.index(num)

if __name__ == "__main__":
    assert solution("210022", 3) == 3
    assert solution("1211", 10) == 1
    print("All tests passed")
