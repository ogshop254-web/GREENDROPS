from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message and main menu."""

    keyboard = [
        [InlineKeyboardButton("🛍️ Products", callback_data="MENU_PRODUCTS")],
        [InlineKeyboardButton("🛒 Cart", callback_data="MENU_CART")],
        [InlineKeyboardButton("📦 My Orders", callback_data="MENU_ORDERS")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Reply with menu
    await update.message.reply_text(
        "👋 Welcome to the Shop Bot!\nPlease choose an option:",
        reply_markup=reply_markup,
    )


def register_start_handler(application):
    """Register /start command handler."""
    application.add_handler(CommandHandler("start", start))
