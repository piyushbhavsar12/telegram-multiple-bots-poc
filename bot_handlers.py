import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    logger.info("Received /start command")
    try:
        await update.message.reply_text("Hello! This is your bot speaking.")
        logger.info("Sent reply to /start command")
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
 
async def handle_message(update: Update, context):
    logger.info(f"Received message: {update.message.text}")
    try:
        await update.message.reply_text(f"You said: {update.message.text}")
        logger.info("Sent reply to message")
    except Exception as e:
        logger.error(f"Error in handle_message: {str(e)}")

def create_bot(token):
    logger.info(f"Creating bot with token: {token[:5]}...")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Handlers added to application")
    return application