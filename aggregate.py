import csv
import sys
import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mydatabase"
    )

def calculate_stats(start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Получаем статистику по дням
    cursor.execute("""
        SELECT 
            DATE(action_time) AS day,
            COUNT(CASE WHEN action_id = 1 THEN 1 END) AS registrations,
            COUNT(CASE WHEN action_id = 8 AND user_id IS NULL THEN 1 END) AS anonymous_messages,
            COUNT(CASE WHEN action_id = 8 THEN 1 END) AS total_messages,
            COUNT(CASE WHEN action_id = 5 AND server_response = 'success' THEN 1 END) AS topics_created
        FROM user_logs
        WHERE DATE(action_time) BETWEEN %s AND %s
        GROUP BY DATE(action_time)
        ORDER BY DATE(action_time)
    """, (start_date, end_date))
    
    daily_stats = cursor.fetchall()
    conn.close()
    
    # Рассчитываем проценты и изменения
    result = []
    prev_topics = 0
    
    for day in daily_stats:
        # Процент анонимных сообщений
        anonymous_percent = 0
        if day['total_messages'] > 0:
            anonymous_percent = (day['anonymous_messages'] / day['total_messages']) * 100
        
        # Процент изменения количества тем
        topics_growth = 0
        if prev_topics > 0:
            topics_growth = (day['topics_created'] / prev_topics) * 100
        elif day['topics_created'] > 0:
            topics_growth = 100  # Первый день с темами
        
        result.append({
            'day': day['day'],
            'new_accounts': day['registrations'],
            'anonymous_messages_percent': round(anonymous_percent, 2),
            'total_messages': day['total_messages'],
            'topics_growth_percent': round(topics_growth, 2)
        })
        
        prev_topics += day['topics_created']
    
    return result

def write_to_csv(data, filename='forum_stats.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['day', 'new_accounts', 'anonymous_messages_percent', 
                     'total_messages', 'topics_growth_percent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python aggregate.py <start_date YYYY-MM-DD> <end_date YYYY-MM-DD>")
        sys.exit(1)
    
    try:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        
        # Простая валидация дат
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
        
        if start_date > end_date:
            print("Error: Start date must be before end date")
            sys.exit(1)
            
        stats = calculate_stats(start_date, end_date)
        write_to_csv(stats)
        print(f"Statistics saved to forum_stats.csv")
        
    except ValueError as e:
        print(f"Error: Invalid date format. Use YYYY-MM-DD. {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
# Для примера:
# python aggregate.py 2025-01-01 2026-01-31