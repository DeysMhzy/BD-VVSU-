# Мухаметзянов Д.С.
# МПИ-23-ИИ
# ---------------------------------------------------------------------------|
# Общий алгоритм работы:
#    Создаётся экземпляр CatFactProcessor
#    Вызывается get_fact() для получения факта
#    Факт сохраняется и может быть проанализирован через get_fact_analysis()
#    Все действия логируются
#    Тесты проверяют все возможные сценарии работы
# ---------------------------------------------------------------------------|
# Код демонстрирует:
#    Работу с внешним API
#    Обработку ошибок
#    Анализ текстовых данных
#    Модульное тестирование с моками
#    Логирование работы программы
# ---------------------------------------------------------------------------|

import requests
from collections import Counter
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class APIError(Exception):
    pass

# Инициализирует пустую строку last_fact для хранения последнего факта
class CatFactProcessor:
    def __init__(self):
        self.last_fact = ""
        logging.debug("1. Инициализация CatFactProcessor завершена.")
# Делает GET-запрос к API catfact.ninja
# Проверяет успешность запроса
# Сохраняет факт в self.last_fact
# Возвращает факт
    def get_fact(self):
        logging.debug("2. Попытка получить факт о кошках.")
        try:
            response = requests.get("https://catfact.ninja/fact")
            response.raise_for_status()
            data = response.json()
            self.last_fact = data["fact"]
            logging.debug(f"3. Получен факт: {self.last_fact}")
            return self.last_fact
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            raise APIError(f"Ошибка при запросе к API: {e}") from e
# Проверяет наличие факта
# Если нет - возвращает пустой результат
# Иначе считает длину и частоту букв (в нижнем регистре)
# Возвращает словарь с результатами анализа
    def get_fact_analysis(self):
        logging.debug("4. Анализ последнего факта о кошках.")
        if not self.last_fact:
            logging.debug("5. Факт отсутствует для анализа.")
            return {"length": 0, "letter_frequencies": {}}
        fact_length = len(self.last_fact)
        letter_frequencies = dict(Counter(self.last_fact.lower()))
        logging.debug(f"6. Длина факта: {fact_length}, Частота букв: {letter_frequencies}")
        return {
            "length": fact_length,
            "letter_frequencies": letter_frequencies,
        }

# Тестирование класса CatFactProcessor
import unittest
from unittest.mock import patch, Mock

class TestCatFactProcessor(unittest.TestCase):
# Мокает requests.get
# Проверяет корректность сохранения и возврата факта
    @patch('requests.get')
    def test_get_fact_success(self, mock_get):
        logging.debug("7. Тестирование успешного получения факта.")
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"fact": "Cats are great!"}
        mock_get.return_value = mock_response

        processor = CatFactProcessor()
        fact = processor.get_fact()

        self.assertEqual(fact, "Cats are great!")
        self.assertEqual(processor.last_fact, "Cats are great!")

    @patch('requests.get')
# Имитирует ошибку соединения
# Проверяет выбрасывание APIError
    def test_get_fact_api_error(self, mock_get):
        logging.debug("8. Тестирование обработки ошибок API.")
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")
        processor = CatFactProcessor()
        with self.assertRaises(APIError) as context:
            processor.get_fact()

        self.assertTrue("Ошибка при запросе к API:" in str(context.exception))
# Проверяет возврат пустого результата при отсутствии факта
    def test_get_fact_analysis_no_fact(self):
        logging.debug("9. Тестирование анализа факта без факта.")
        processor = CatFactProcessor()
        analysis = processor.get_fact_analysis()
        self.assertEqual(analysis, {"length": 0, "letter_frequencies": {}})
# Мокает получение конкретного факта
# Проверяет корректность анализа:
#   Длину строки
#   Частоту каждого символа (включая пробелы и знаки)
    @patch('requests.get')
    def test_get_fact_analysis_with_fact(self, mock_get):
        logging.debug("10. Тестирование анализа факта с фиксированным фактом.")
        fixed_fact = "Cats are great!"  # Фиксированный факт
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"fact": fixed_fact}
        mock_get.return_value = mock_response

        processor = CatFactProcessor()
        processor.get_fact()  # Получаем факт

        analysis = processor.get_fact_analysis()
        # Правильные частоты для "Cats are great!":
        expected_frequencies = {
            'c': 1, 'a': 3, 't': 2, 's': 1, 
            ' ': 2, 'r': 2, 'e': 2, 'g': 1, '!': 1
        }

        self.assertEqual(analysis["length"], len(fixed_fact))
        self.assertEqual(analysis["letter_frequencies"], expected_frequencies)
        
if __name__ == '__main__':
    unittest.main()


