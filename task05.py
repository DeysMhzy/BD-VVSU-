"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List

def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    print(f"Исходный массив: {nums}, максимальная длина подмассива: {k}")
    
    n = len(nums)
    max_sum = float('-inf')  # Инициализируем максимальную сумму минимально возможным значением
    current_sum = 0
    
    # Используем скользящее окно для нахождения максимальной суммы подмассива
    for i in range(n):
        current_sum += nums[i]
        print(f"Добавляем {nums[i]} к текущей сумме: {current_sum}")
        
        # Если длина подмассива превышает k, вычитаем элемент, который выходит за пределы окна
        if i >= k:
            current_sum -= nums[i - k]
            print(f"Вычитаем {nums[i - k]} из текущей суммы: {current_sum}")
        
        # Обновляем максимальную сумму, если текущая сумма больше
        if current_sum > max_sum:
            max_sum = current_sum
            print(f"Новая максимальная сумма: {max_sum}")
    
    return max_sum

# Примеры последовательностей
valid_nums = [1, 3, -1, -3, 5, 3, 6, 7]  # Правильный пример
invalid_nums = [1, -1, 2, -2, 3, -3, 4]   # Неправильный пример

k = 3

# Проверка правильной последовательности
print("Проверка правильной последовательности:")
result_valid = find_maximal_subarray_sum(valid_nums, k)
print(f"Максимальная сумма подмассива (правильный пример): {result_valid}\n")

# Проверка неправильной последовательности
print("Проверка неправильной последовательности:")
result_invalid = find_maximal_subarray_sum(invalid_nums, k)
print(f"Максимальная сумма подмассива (неправильный пример): {result_invalid}")