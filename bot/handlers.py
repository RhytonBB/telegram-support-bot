from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from telegram.constants import ParseMode
from .db import create_ticket, generate_chat_url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Создать обращение", callback_data="create_ticket")]
    ]
    
    await update.message.reply_text(
        "Добро пожаловать в службу поддержки!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def create_ticket_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    ticket_id = create_ticket(user_id)
    chat_url = generate_chat_url(ticket_id)
    
    await query.edit_message_text(
        f"✅ Обращение #{ticket_id} создано.\n"
        f"Перейдите по ссылке для общения с оператором:\n{chat_url}"
    )

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(create_ticket_callback, pattern="^create_ticket$"))