import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from . import config, db, handlers

print("BOT_TOKEN:", repr(config.BOT_TOKEN))
def main():
    # Инициализация базы данных
    db.init_db()

    # Логирование
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Создание приложения Telegram
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Регистрация хендлеров
    handlers.register_handlers(app)

    # Обработка команды /start (приветствие + кнопка)
    async def start(update, context):
        await update.message.reply_text(
            "Привет! Нажмите /support для обращения в техподдержку."
        )

    app.add_handler(CommandHandler("start", start))

    # Запуск бота
    logging.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
