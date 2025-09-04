# nums = [1, 1, 2, 2, 3, 4, 4, 5]
from typing import Any


def rm_duplicates(nums: list[int]) -> Any:
    if not nums:
        return 0
    elif len(nums) == 1:
        return 1

    flag = 1
    for num in range(1, len(nums)):
        if nums[num] != nums[num - 1]:
            nums[flag] = nums[num]
            flag += 1
    return [flag, nums[0:flag]]

if __name__ == "__main__":
    assert rm_duplicates([1, 2, 3, 4]) == [4, [1, 2, 3, 4]]
    assert rm_duplicates([1, 1, 2, 2, 3, 4, 4, 5]) == [5, [1, 2, 3, 4, 5]]
    assert rm_duplicates([1, 1, 2, 2, 3, 4, 4, 5]) == [5, [1, 2, 3, 4, 5]]
    assert rm_duplicates([]) == 0
    assert rm_duplicates([1]) == 1
