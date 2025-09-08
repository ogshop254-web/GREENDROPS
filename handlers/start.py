from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from handlers.menu import menu   # 👈 import the menu function


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message and show menu right away."""
    await update.message.reply_text("👋 Welcome to the Shop Bot!")

    # Show menu directly
    await menu(update, context)


def register_start_handler(application):
    application.add_handler(CommandHandler("start", start))
