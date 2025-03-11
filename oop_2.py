"""
В этом задании будем улучшать нашу систему классов из задания прошлой лекции
(Student, Teacher, Homework)
Советую обратить внимание на defaultdict из модуля collection для
использования как общую переменную


1. Как то не правильно, что после do_homework мы возвращаем все тот же
объект - будем возвращать какой-то результат работы (HomeworkResult)

HomeworkResult принимает объект автора задания, принимает исходное задание
и его решение в виде строки
Атрибуты:
    homework - для объекта Homework, если передан не этот класс -  выкинуть
    подходящие по смыслу исключение с сообщением:
    'You gave a not Homework object'

    solution - хранит решение ДЗ как строку
    author - хранит объект Student
    created - c точной датой и временем создания

2. Если задание уже просрочено хотелось бы видеть исключение при do_homework,
а не просто принт 'You are late'.
Поднимайте исключение DeadlineError с сообщением 'You are late' вместо print.

3. Student и Teacher имеют одинаковые по смыслу атрибуты
(last_name, first_name) - избавиться от дублирования с помощью наследования

4.
Teacher
Атрибут:
    homework_done - структура с интерфейсом как в словаря, сюда поподают все
    HomeworkResult после успешного прохождения check_homework
    (нужно гаранитровать остутствие повторяющихся результатов по каждому
    заданию), группировать по экземплярам Homework.
    Общий для всех учителей. Вариант ипользования смотри в блоке if __main__...
Методы:
    check_homework - принимает экземпляр HomeworkResult и возвращает True если
    ответ студента больше 5 символов, так же при успешной проверке добавить в
    homework_done.
    Если меньше 5 символов - никуда не добавлять и вернуть False.

    reset_results - если передать экземпряр Homework - удаляет только
    результаты этого задания из homework_done, если ничего не передавать,
    то полностью обнулит homework_done.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""


import datetime
from collections import defaultdict

# Определяем исключение для обработки просроченных заданий
class DeadlineError(Exception):
    pass

# Класс для задания домашней работы
class Homework:
    def __init__(self, task, deadline):
        self.task = task  # Задание
        self.deadline = deadline  # Дата и время дедлайна

    # Метод для проверки, просрочено ли задание
    def is_late(self):
        return datetime.datetime.now() > self.deadline

# Класс для результата выполнения домашней работы
class HomeworkResult:
    def __init__(self, author, homework, solution):
        # Проверяем, является ли переданный объект заданием
        if not isinstance(homework, Homework):
            raise ValueError('Вы передали не объект Homework')
        # Проверяем, не просрочено ли задание
        if homework.is_late():
            raise DeadlineError('Вы опоздали с выполнением задания')

        self.homework = homework  # Сохраняем объект задания
        self.solution = solution  # Сохраняем решение
        self.author = author  # Сохраняем автора
        self.created = datetime.datetime.now()  # Время создания результата

# Базовый класс для людей (студентов и учителей)
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name  # Имя
        self.last_name = last_name  # Фамилия

# Класс для студентов, наследуется от Person
class Student(Person):
    # Метод для выполнения домашней работы
    def do_homework(self, homework, solution):
        print(f"{self.first_name} {self.last_name} выполняет домашнюю работу: {homework.task}")
        return HomeworkResult(self, homework, solution)

# Класс для учителей, наследуется от Person
class Teacher(Person):
    homework_done = defaultdict(set)  # Структура для хранения выполненных заданий

    # Метод для проверки выполненной домашней работы
    def check_homework(self, homework_result):
        print(f"Проверка домашней работы от {homework_result.author.first_name} {homework_result.author.last_name}")
        if len(homework_result.solution) > 5:
            self.homework_done[homework_result.homework].add(homework_result)  # Добавляем результат в структуру
            print("Работа принята.")
            return True
        print("Работа отклонена: слишком короткое решение.")
        return False

    # Метод для сброса результатов
    @classmethod
    def reset_results(cls, homework=None):
        if homework:
            cls.homework_done.pop(homework, None)  # Удаляем результаты для конкретного задания
            print(f"Результаты для задания '{homework.task}' удалены.")
        else:
            cls.homework_done.clear()  # Полностью очищаем результаты
            print("Все результаты очищены.")

    # Метод для создания домашней работы
    def create_homework(self, task, days):
        deadline = datetime.datetime.now() + datetime.timedelta(days=days)  # Устанавливаем дедлайн
        return Homework(task, deadline)

if __name__ == '__main__':
    # Создаем учителей и студентов
    opp_teacher = Teacher('Daniil', 'Shadrin')
    advanced_python_teacher = Teacher('Aleksandr', 'Smetanin')

    lazy_student = Student('Roman', 'Petrov')
    good_student = Student('Lev', 'Sokolov')

    # Создаем задания
    oop_hw = opp_teacher.create_homework('Learn OOP', 1)
    docs_hw = opp_teacher.create_homework('Read docs', 5)

    # Студенты выполняют задания
    result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
    result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
    result_3 = lazy_student.do_homework(docs_hw, 'done')

    # Проверяем обработку исключений
    try:
        result_4 = HomeworkResult(good_student, "fff", "Solution")
    except Exception as e:
        print(f'Произошла ошибка: {e}')

    # Учитель проверяет домашние работы
    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = advanced_python_teacher.homework_done
    assert temp_1 == temp_2  # Проверяем, что результаты совпадают

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    # Выводим результаты выполненной домашней работы
    print(opp_teacher.homework_done[oop_hw])
    Teacher.reset_results()  # Сбрасываем результаты