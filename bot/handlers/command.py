from telegram import Update
from telegram.ext import ContextTypes
from db.database import Database
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration for the database connection using environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

# Retrieve the bot's username from the environment variables
BOT_USERNAME: str = os.getenv('BOT_USERNAME')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract user information from the update
    user = update.message.from_user

    # Open a database connection using the 'with' context
    with Database(**DB_CONFIG) as db:
        # Check if the user is already registered in the database
        if not db.is_user_registered(user.id):
            # If not registered, add the user to the database
            db.register_user(user.id, user.username, user.first_name, user.last_name)

    # Send a welcome message back to the user
    await update.message.reply_text(f"Olá {user.first_name}! Como posso te ajudar?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a help message back to the user
    await update.message.reply_text(f"Envie qualquer mensagem que irei responder de volta para você!")
