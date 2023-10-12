from telegram import Update
from telegram.ext import ContextTypes
from bot.handlers.gptconnection import gpt_completion
from db.database import Database
from dotenv import load_dotenv
import os
import speech_recognition as sr

# Load environment variables from the .env file
load_dotenv()

# Configure database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

# Fetch the bot's username from environment variables
BOT_USERNAME: str = os.getenv('BOT_USERNAME') 

# Function to handle errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Print the error when an exception occurs"""
    print(f'Update {update} caused an error {context.error}')

# Main function to handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle text or voice messages from users.
    Store user messages and bot responses in the database.
    Respond back to the user with a message.
    """
    
    # Check if the incoming message is a voice message
    if update.message.voice:
        bot_response, message_id = await handle_voice(update, context)
    else:
        # If not voice, store the text message in the database and retrieve its ID
        with Database(**DB_CONFIG) as db:
            message_id = db.store_message(update.message.from_user.id, update.message.text)

        # Get a response using the GPT model
        bot_response: str = gpt_completion(update.message.text)

    # Store the bot's response in the database
    with Database(**DB_CONFIG) as db:
        db.store_response(update.message.from_user.id, message_id, update.message.text, bot_response)

    # Send the response back to the user
    await update.message.reply_text(bot_response)

# Function to handle voice messages
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Convert voice messages to text, get a response and store in the database."""
    
    # Download the voice message
    audio_file = await update.message.voice.get_file()
    await audio_file.download_to_drive('voice.ogg')

    # Convert the .ogg file to .wav format for processing
    os.system("ffmpeg -i voice.ogg voice.wav")

    # Use the Speech Recognition library to convert voice to text
    r = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        audio = r.record(source)
        try:
            user_message = r.recognize_google(audio, language='pt-BR')
        except sr.UnkwonValueError:  # Note: Typo here, should be "UnknownValueError"
            user_message = "err"

    # Cleanup: Delete the audio files after processing
    os.remove("voice.ogg")
    os.remove("voice.wav")

    # Process the recognized text and get a response
    if user_message != "err":
        with Database(**DB_CONFIG) as db:
            message_id = db.store_message(update.message.from_user.id, user_message)
            
        # Check for mentions in group chats
        if update.message.chat.type == 'group':
            if BOT_USERNAME in user_message:
                new_text: str = user_message.replace(BOT_USERNAME,'').strip()
                bot_response: str = gpt_completion(new_text)
            else:
                return
        else:
            bot_response: str = gpt_completion(user_message)

        return bot_response, message_id
