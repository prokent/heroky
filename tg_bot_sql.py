from dotenv import load_dotenv
import os
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')  # Путь к базе данных

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я ваш бот.')

async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        conn = sqlite3.connect(DATABASE_URL)  # Подключение к базе данных
        cursor = conn.cursor()
        cursor.execute('SELECT username, email FROM user')
        users = cursor.fetchall()
        conn.close()
        
        if users:
            user_list = '\n'.join([f'{i+1}. {user[0]} - {user[1]}' for i, user in enumerate(users)])
            await update.message.reply_text(f'📋 **Список пользователей**:\n\n{user_list}', parse_mode='Markdown')
        else:
            await update.message.reply_text('Пользователи не найдены.')
    except Exception as e:
        await update.message.reply_text(f'Ошибка при получении пользователей: {e}')

async def get_articles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text('Пытаюсь получить статьи из базы данных...')
        conn = sqlite3.connect(DATABASE_URL)  # Подключение к базе данных
        cursor = conn.cursor()
        cursor.execute('SELECT title, intro, text FROM article')
        articles = cursor.fetchall()
        conn.close()
        
        if articles:
            article_list = '\n\n'.join([f'📖 **Заголовок**: {article[0]}\n**Интро**: {article[1]}\n**Текст**: {article[2]}' for article in articles])
            await update.message.reply_text(article_list, parse_mode='Markdown')
        else:
            await update.message.reply_text('Статей не найдено.')
    except Exception as e:
        await update.message.reply_text(f'Ошибка при получении статей: {e}')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_users", get_users))
    app.add_handler(CommandHandler("get_articles", get_articles))
    
    app.run_polling()

if __name__ == '__main__':
    main()
