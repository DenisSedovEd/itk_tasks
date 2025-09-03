# nums = [2, 7, 11, 15]
# target = 9


def two_sum_v1(nums: list, target: int) -> list:
    nums_len = len(nums)
    for idx in range(nums_len):
        for idy in range(idx + 1, nums_len):
            if nums[idx] + nums[idy] == target:
                return [idx, idy]
    return []


def two_sum_v2(nums: list, target: int) -> list:
    res = {}
    for idx, num in enumerate(nums):
        subtraction = target - num
        if subtraction in res:
            return [res[subtraction], idx]
        res[num] = idx
    return []


if __name__ == "__main__":
    assert two_sum_v1(nums=[2, 7, 11, 15], target=17) == [0, 3]
    assert two_sum_v1(nums=[2, 7, 11, 15], target=9) == [0, 1]
    assert two_sum_v1(nums=[2, 7, 11, 15], target=26) == [2, 3]
    assert two_sum_v1(nums=[2, 7, 11, 15], target=22) == [1, 3]
    assert two_sum_v1(nums=[2, 7, 11, 15], target=0) == []

    assert two_sum_v2(nums=[2, 7, 11, 15], target=17) == [0, 3]
    assert two_sum_v2(nums=[2, 7, 11, 15], target=9) == [0, 1]
    assert two_sum_v2(nums=[2, 7, 11, 15], target=26) == [2, 3]
    assert two_sum_v2(nums=[2, 7, 11, 15], target=22) == [1, 3]
    assert two_sum_v2(nums=[2, 7, 11, 15], target=0) == []
