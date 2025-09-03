# nums = [2, 7, 11, 15]
# target = 9

def two_sum(nums: list, target: int) -> list | str:
    result = None
    for idx, _ in enumerate(nums):
        if idx == (len(nums)-1):
            result = 'Такой пары нет'
        for idy, _ in enumerate(nums):
            if nums[idx] + nums[idy] == target:
                return [idx, idy]
    return result

if __name__ == '__main__':
    assert two_sum(nums=[2, 7, 11, 15], target=17) == [0, 3]
    assert two_sum(nums=[2, 7, 11, 15], target=9) == [0, 1]
    assert two_sum(nums=[2, 7, 11, 15], target=26) == [2, 3]
    assert two_sum(nums=[2, 7, 11, 15], target=22) == [1, 3]
    assert two_sum(nums=[2, 7, 11, 15], target=0) == 'Такой пары нет'


