"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"

Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished"

    [[-, -, o],
     [-, o, o],
     [x, x, x]]

     Return value should be "x wins!"

"""

from typing import List

def print_board(board: List[List[str]]):
    """Функция для визуального отображения доски."""
    print("  1 | 2 | 3")  # Заголовок для столбцов
    print("----------------")
    for index, row in enumerate(board):
        print(f"{index + 1} | " + " | ".join(row))
        print("----------------")  # Разделитель между строками

def tic_tac_toe_checker(board: List[List[str]]) -> str:
    """Проверяет состояние игры в крестики-нолики."""
    # Проверяем строки на победителя
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '-':
            return f"{row[0]} wins!"
    
    # Проверяем столбцы на победителя
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '-':
            return f"{board[0][col]} wins!"
    
    # Проверяем диагонали на победителя
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '-':
        return f"{board[0][0]} wins!"
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '-':
        return f"{board[0][2]} wins!"
    
    # Проверяем на ничью или незавершенную игру
    for row in board:
        if '-' in row:
            return "unfinished"
    
    return "draw!"

def main():
    # Инициализация пустой доски
    board = [['-' for _ in range(3)] for _ in range(3)]
    current_player = 'x'  # Начинаем с игрока 'x'

    while True:
        print_board(board)  # Отображаем текущую доску
        print(f"Текущий игрок: {current_player}")
        
        # Запрашиваем ввод от игрока
        try:
            row = int(input("Введите номер строки (1, 2, 3): ")) - 1  # Преобразуем в 0-индексацию
            col = int(input("Введите номер столбца (1, 2, 3): ")) - 1  # Преобразуем в 0-индексацию
        except ValueError:
            print("Пожалуйста, введите корректные числа.")
            continue
        
        # Проверяем, что введенные координаты находятся в пределах доски и клетка свободна
        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == '-':
            board[row][col] = current_player  # Устанавливаем символ текущего игрока
        else:
            print("Некорректный ход, попробуйте снова.")
            continue
        
        # Проверяем состояние игры
        result = tic_tac_toe_checker(board)
        if result != "unfinished":
            print_board(board)  # Отображаем финальную доску
            print(result)  # Выводим результат игры
            break  # Завершаем игру

        # Меняем игрока
        current_player = 'o' if current_player == 'x' else 'x'

if __name__ == "__main__":
    main()