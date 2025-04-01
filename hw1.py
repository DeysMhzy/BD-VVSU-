"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""

from typing import List
import string
from collections import Counter
import os

def decode_unicode(text: str) -> str:
    # Декодируем текст, заменяя escape-последовательности на соответствующие символы
    return text.encode().decode('unicode_escape')

def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Декодируем текст
    text = decode_unicode(text)
    
    words = text.split()
    unique_words = [(word, len(set(word))) for word in words]
    unique_words.sort(key=lambda x: (-x[1], -len(x[0])))
    longest_diverse_words = [word[0] for word in unique_words[:10]]
    
    print("10 самых длинных слов с наибольшим количеством уникальных символов:", longest_diverse_words)
    return longest_diverse_words

def get_rarest_char(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Декодируем текст
    text = decode_unicode(text)
    
    char_count = Counter(text)
    rarest_char = min(char_count, key=char_count.get)
    
    print("Редчайший символ в документе:", rarest_char)
    return rarest_char

def count_punctuation_chars(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Декодируем текст
    text = decode_unicode(text)
    
    punctuation_count = sum(1 for char in text if char in string.punctuation)
    
    print("Количество знаков препинания:", punctuation_count)
    return punctuation_count

def count_non_ascii_chars(file_path: str) -> int:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Декодируем текст
    text = decode_unicode(text)
    
    non_ascii_count = sum(1 for char in text if ord(char) > 127)
    
    print("Количество не ASCII символов:", non_ascii_count)
    return non_ascii_count

def get_most_common_non_ascii_char(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Декодируем текст
    text = decode_unicode(text)
    
    non_ascii_chars = [char for char in text if ord(char) > 127]
    
    if not non_ascii_chars:
        print("Нет не ASCII символов в документе.")
        return ''
    
    non_ascii_count = Counter(non_ascii_chars)
    most_common_non_ascii_char = non_ascii_count.most_common(1)[0][0]
    
    print("Самый распространенный не ASCII символ:", most_common_non_ascii_char)
    return most_common_non_ascii_char

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'data.txt')  # Полный путь к файлу data.txt
    
    print("Путь к файлу:", file_path)
    
    get_longest_diverse_words(file_path)
    get_rarest_char(file_path)
    count_punctuation_chars(file_path)
    count_non_ascii_chars(file_path)
    get_most_common_non_ascii_char(file_path)