# nums = [10, 9, 2, 5, 3, 7, 101, 18]
# 3   Подпоследовательность: [3, 7, 101]

def longest_sequence(nums: list[int]) -> int:
    if not nums:
        return 0

    max_len = 1
    current_len = 1
    for i in range(0, len(nums) -1 ):
        if nums[i] < nums[i+1]:
            current_len += 1
            max_len = max(max_len, current_len)
        else:
            current_len = 1

    return max_len


if __name__ == '__main__':
    assert longest_sequence([1, 1, 2]) == 2
    assert longest_sequence([1, 1, 2, 3, 7, 0, -5]) == 4
    assert longest_sequence([10, 9, 2, 5, 3, 7, 101, 18]) == 3
    assert longest_sequence([]) == 0