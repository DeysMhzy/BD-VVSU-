"""
Необходимо создать 3 класса и взаимосвязь между ними (Student, Teacher,
Homework)
Наследование в этой задаче использовать не нужно.
Для работы с временем использовать модуль datetime

1. Homework принимает на вход 2 атрибута: текст задания и количество дней
на это задание
Атрибуты:
    text - текст задания
    deadline - хранит объект datetime.timedelta с количеством
    дней на выполнение
    created - c точной датой и временем создания
Методы:
    is_active - проверяет не истело ли время на выполнение задания,
    возвращает boolean

2. Student
Атрибуты:
    last_name
    first_name
Методы:
    do_homework - принимает объект Homework и возвращает его же,
    если задание уже просрочено, то печатет 'You are late' и возвращает None

3. Teacher
Атрибуты:
     last_name
     first_name
Методы:
    create_homework - текст задания и количество дней на это задание,
    возвращает экземпляр Homework
    Обратите внимание, что для работы этого метода не требуется сам объект.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""
import datetime

# Класс - Домашка
class Homework:
    def __init__(self, text, days):
        # Инициализация задания с текстом, сроком выполнения и временем создания
        self.text = text
        self.deadline = datetime.timedelta(days=days)
        self.created = datetime.datetime.now()
        print(f"[DEBUG] Задание создано: '{self.text}', Срок выполнения: {self.deadline}, Создано в: {self.created}")

    def is_active(self):
        # Проверка, активно ли задание (не истек ли срок выполнения)
        active = datetime.datetime.now() < self.created + self.deadline
        print(f"[DEBUG] Проверка активности задания '{self.text}': {active}")
        return active

# Класс - Студенты
class Student:
    def __init__(self, first_name, last_name):
        # Инициализация студента с именем и фамилией
        self.first_name = first_name
        self.last_name = last_name
        print(f"[DEBUG] Студент создан: {self.first_name} {self.last_name}")

    def do_homework(self, homework):
        # Попытка выполнить задание
        print(f"[DEBUG] Студент {self.first_name} пытается выполнить задание: '{homework.text}'")
        if homework.is_active():
            print(f"[DEBUG] Задание '{homework.text}' выполнено студентом {self.first_name}.")
            return homework
        else:
            print('Вы опоздали')
            return None

# Класс - Учитель
class Teacher:
    def __init__(self, first_name, last_name):
        # Инициализация учителя с именем и фамилией
        self.first_name = first_name
        self.last_name = last_name
        print(f"[DEBUG] Учитель создан: {self.first_name} {self.last_name}")

    def create_homework(self, text, days):
        # Создание задания с текстом и сроком выполнения
        print(f"[DEBUG] Учитель {self.first_name} создает задание: '{text}' с сроком выполнения {days} дней.")
        return Homework(text, days)


if __name__ == '__main__':
    # Создание экземпляров учителя и студента
    teacher = Teacher('Daniil', 'Shadrin')
    student = Student('Roman', 'Petrov')

    # Создание просроченного задания
    expired_homework = teacher.create_homework('Learn functions', 0)
    print(expired_homework.created)  # Например: 2019-05-26 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'

    # Создание задания через функцию
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    print(oop_homework.deadline)  # 5 дней, 0:00:00

    # Студент пытается выполнить задания
    student.do_homework(oop_homework)
    student.do_homework(expired_homework)  # Вы опоздали
