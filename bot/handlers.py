from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler

from .db import create_ticket, get_archived_tickets, generate_chat_url


async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /support или кнопку 'Тех поддержка'"""
    user_id = update.effective_user.id

    # Кнопка "Написать обращение"
    keyboard = [
        [InlineKeyboardButton("📝 Написать обращение", callback_data="create_ticket")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )

    # Получаем список архивных обращений
    archived = get_archived_tickets(user_id)

    if archived:
        lines = ["📁 *Архивные обращения:*"]
        for ticket_id, chat_url in archived:
            lines.append(f"• [Обращение №{ticket_id}]({chat_url})")
        text = "\n".join(lines)
    else:
        text = "_У вас пока нет архивных обращений._"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def create_ticket_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создание нового обращения"""
    query = update.callback_query
    user_id = query.from_user.id

    ticket_id = create_ticket(user_id)
    chat_url = generate_chat_url(user_id, ticket_id)

    await query.answer()
    await query.message.reply_text(
        f"✅ Обращение №{ticket_id} создано.\n"
        f"Перейдите по ссылке для общения с оператором:\n{chat_url}"
    )


def register_handlers(app):
    """Регистрация хендлеров"""
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CallbackQueryHandler(create_ticket_callback, pattern="^create_ticket$"))
