import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from bot_tg.request_for_ai import parse_enter_message, get_message_for_ai
from message_text import START_MESSAGE, HELP

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGE
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP
    )

# Асинхронный обработчик ошибок
async def error_handler(update, context):
    logging.error(f"Произошла ошибка: {context.error}")
    # Опционально: отправьте сообщение пользователю
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Произошла ошибка. Пожалуйста, попробуйте позже."
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_from_bot = update.message.text
    allies, enemy = parse_enter_message(message_from_bot)
    text_for_ai = get_message_for_ai(allies, enemy)
    # answer = request_gpt(text_for_ai)
    print()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':

    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    application.add_error_handler(error_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),  echo)
    application.add_handler(echo_handler)

    application.run_polling()

