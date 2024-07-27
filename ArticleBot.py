from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3
import os
from dotenv import load_dotenv

# Статический токен бота
load_dotenv()  # Загружает переменные из файла .env

TOKEN = '7112295260:AAFpQ1Cqo31Odq-69t54stivkoJ21eTJkug'

# Полный путь к базе данных
DB_PATH = '/Users/pro.kent/Documents/GitHub/lilia/blog.db'

def check_database_exists(db_path):
    """ Проверяет, существует ли файл базы данных. """
    if not os.path.isfile(db_path):
        raise FileNotFoundError(f"Файл базы данных не найден: {db_path}")

def initialize_database():
    """ Инициализирует базу данных, если она существует. """
    check_database_exists(DB_PATH)  # Проверяем существование файла базы данных
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS article (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                intro TEXT NOT NULL,
                text TEXT NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        conn.close()

def get_articles():
    """ Получает статьи из базы данных. """
    check_database_exists(DB_PATH)  # Проверяем существование файла базы данных
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title, intro, text FROM article")
        articles = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        articles = []
    finally:
        conn.close()
    return articles

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обрабатывает команду /start. """
    await update.message.reply_text('Привет! Используйте команду /articles, чтобы получить список статей.')

async def articles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обрабатывает команду /articles. """
    articles = get_articles()
    if articles:
        for title, intro, text in articles:
            # Отправка сообщений с использованием Markdown
            await update.message.reply_text(f'*Заголовок:* {title}\n*Интро:* {intro}\n\n*Текст:* {text}', parse_mode='Markdown')
    else:
        await update.message.reply_text('Статей пока нет.')

def main() -> None:
    """ Основная функция для запуска бота. """
    # Проверяем существование базы данных перед инициализацией
    try:
        check_database_exists(DB_PATH)
    except FileNotFoundError as e:
        print(e)
        return  # Завершаем выполнение, так как база данных не найдена

    # Инициализация базы данных
    initialize_database()

    # Инициализация Application
    application = Application.builder().token(TOKEN).build()

    # Определение команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("articles", articles))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
