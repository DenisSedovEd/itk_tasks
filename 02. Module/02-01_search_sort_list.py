"""
Задача - Поиск элемента в упорядоченном списке
Дан отсортированный список чисел, например: [1, 2, 3, 45, 356, 569, 600, 705, 923]
Список может содержать миллионы элементов.
Необходимо написать функцию search(number: id) -> bool которая принимает число number
и возвращает True если это число находится в этом списке.
Требуемая сложность алгоритма O(log n).
"""


def quick_search(numbers: list[int], number: int) -> bool:
    left = 0
    right = len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == number:
            return True
        elif number < numbers[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False


if __name__ == "__main__":
    numbers_list = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    assert quick_search(numbers_list, 1) == True
    assert quick_search(numbers_list, 2) == True
    assert quick_search(numbers_list, 705) == True
    assert quick_search(numbers_list, 7) == False
    # print(quick_search(numbers_list, 600))
