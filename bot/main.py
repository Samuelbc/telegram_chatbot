import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers.command import start_command, help_command
from bot.handlers.message import handle_message, error
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch bot configuration values from environment variables
TOKEN: str = os.getenv('TOKEN')
BOT_USERNAME: str = os.getenv('BOT_USERNAME')

def main() -> None:
    """Main function to set up and start the Telegram bot."""
    
    # Initialize the bot with the given token
    print('Starting bot...')
    application = (
        Application.builder()
        .token(os.getenv('TOKEN'))
        .build()
    )

    # Register command handlers for the "/start" and "/help" commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Register a message handler that will process all types of messages
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    # Register an error handler to handle exceptions
    application.add_error_handler(error)

    # Start polling for new messages from Telegram servers
    print('Polling...')
    application.run_polling(poll_interval=3)


# If this script is run as the main module, execute the main function
if __name__ == '__main__':
    asyncio.run(main())
