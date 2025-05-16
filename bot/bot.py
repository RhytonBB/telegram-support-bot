import logging
import threading
from telegram.ext import ApplicationBuilder, CommandHandler
from . import config, db, handlers, api

def run_flask():
    api.app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )

def main():
    # Инициализация базы данных
    db.init_db()

    # Настройка логирования
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Запуск Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Создание Telegram бота
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Регистрация обработчиков
    handlers.register_handlers(app)

    # Запуск бота
    logging.info("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()