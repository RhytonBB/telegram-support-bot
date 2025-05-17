import logging
import threading
from telegram.ext import ApplicationBuilder, CommandHandler, Application
from telegram.error import Conflict
from . import config, db, handlers, api
from telegram import Update

def run_flask():
    api.app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )

async def post_init(application: Application):
    """Очистка очереди обновлений при запуске"""
    await application.bot.delete_webhook(drop_pending_updates=True)
    logging.info("Очередь обновлений очищена")

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

    # Создание и настройка бота
    application = ApplicationBuilder() \
        .token(config.BOT_TOKEN) \
        .post_init(post_init) \
        .build()

    # Регистрация обработчиков
    handlers.register_handlers(application)

    # Запуск бота с обработкой ошибок
    try:
        logging.info("Бот запущен...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            close_loop=False,
            stop_signals=None
        )
    except Conflict as e:
        logging.error(f"Конфликт: {e}. Возможно, бот уже запущен.")
    except Exception as e:
        logging.error(f"Ошибка: {e}")

if __name__ == "__main__":
    main()