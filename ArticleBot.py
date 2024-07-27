import os
from dotenv import load_dotenv
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загружаем переменные из файла .env
load_dotenv()

# Статический токен бота
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_telegram_bot_token')

# Полный путь к базе данных из переменной окружения
DB_PATH = '/Users/pro.kent/Documents/GitHub/lilia/blog.db'

def check_database_exists(db_path):
    """ Проверяет, существует ли файл базы данных. """
    return os.path.isfile(db_path)

def initialize_database():
    """ Инициализирует базу данных, если она существует. """
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
    if not check_database_exists(DB_PATH):
        return [], "Файл базы данных не найден. Пожалуйста, попробуйте позже."

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title, intro, text FROM article")
        articles = cursor.fetchall()
        return articles, None
    except sqlite3.Error as e:
        return [], f"Ошибка базы данных: {e}"
    finally:
        conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обрабатывает команду /start. """
    await update.message.reply_text('Привет! Используйте команду /articles, чтобы получить список статей.')

async def articles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обрабатывает команду /articles. """
    articles, error_message = get_articles()
    if error_message:
        await update.message.reply_text(error_message)
    elif articles:
        for title, intro, text in articles:
            # Отправка сообщений с использованием Markdown
            await update.message.reply_text(f'*Заголовок:* {title}\n*Интро:* {intro}\n\n*Текст:* {text}', parse_mode='Markdown')
    else:
        await update.message.reply_text('Статей пока нет.')

def handle_database_errors(func):
    """ Обертка для обработки ошибок базы данных. """
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            await func(update, context)
        except Exception as e:
            error_message = f"Произошла ошибка: {e}"
            await update.message.reply_text(error_message)
    return wrapper

@handle_database_errors
async def start_with_error_handling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обрабатывает команду /start с обработкой ошибок. """
    await start(update, context)

@handle_database_errors
async def articles_with_error_handling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обрабатывает команду /articles с обработкой ошибок. """
    await articles(update, context)

def main() -> None:
    """ Основная функция для запуска бота. """
    # Инициализация базы данных
    initialize_database()

    # Инициализация Application
    application = Application.builder().token(TOKEN).build()

    # Определение команд с обработкой ошибок
    application.add_handler(CommandHandler("start", start_with_error_handling))
    application.add_handler(CommandHandler("articles", articles_with_error_handling))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
