"""
Main entrypoint for the Telegram e-commerce bot.
"""

import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

from database.db import init_db
from handlers.menu import register_start_handler


# -----------------------
# Logging setup
# -----------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# -----------------------
# Main function
# -----------------------
def main():
    # Load environment variables
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN not found in .env file")

    # Init database
    init_db()

    # Create bot application
    application = Application.builder().token(token).build()

    # Register handlers
    register_start_handler(application)

    # Start polling
    logger.info("Bot started. Listening for updates...")
    application.run_polling()

if __name__ == "__main__":
    main()
