import sqlite3

DB_PATH = '/Users/pro.kent/Documents/GitHub/AzEr/blog.db'

def initialize_database():
    """Инициализирует базу данных и создает таблицы, если они не существуют."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Создание таблицы article
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS article (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                intro TEXT NOT NULL,
                text TEXT NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создание таблицы user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        print("Таблицы созданы успешно")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()
    