# nums = [1, 1, 2, 2, 3, 4, 4, 5]


def rm_dublocates(nums: list[int]) -> list[int]:
    result = list(set(nums))
    result.sort()
    return result


if __name__ == "__main__":
    print(rm_dublocates(nums=[1, 1, 2, 2, 3, 4, 4, 5]))
