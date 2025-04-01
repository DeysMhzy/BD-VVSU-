"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence

We guarantee, that the given sequence contain >= 0 integers inside.

"""
from collections.abc import Sequence

def check_fibonacci(data: Sequence[int]) -> bool:
    print(f"Проверяем последовательность: {data}")
    
    # Проверка длины последовательности
    if len(data) < 2:
        print("Последовательность должна содержать как минимум два числа.")
        return len(data) == 0 or data[0] == 0
    
    # Проверка условия Фибоначчи
    for i in range(2, len(data)):
        print(f"Проверяем: {data[i]} == {data[i - 1]} + {data[i - 2]}")
        if data[i] != data[i - 1] + data[i - 2]:
            print(f"Ошибка: {data[i]} не равно {data[i - 1]} + {data[i - 2]}")
            return False
            
    print("Последовательность является последовательностью Фибоначчи.")
    return True

# Примеры последовательностей
valid_sequence = [0, 1, 1, 2, 3, 5, 8, 13]
invalid_sequence = [0, 1, 1, 2, 4, 5, 9]

# Проверка правильной последовательности
print("Проверка правильной последовательности:")
result = check_fibonacci(valid_sequence)
print(f"Результат: {result}\n")

# Проверка неправильной последовательности
print("Проверка неправильной последовательности:")
result = check_fibonacci(invalid_sequence)
print(f"Результат: {result}")