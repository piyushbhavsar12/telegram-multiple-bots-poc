import asyncio
import logging
from fastapi import FastAPI, Request
from newappconfig import BOT_CREDENTIALS
from bot_handlers import create_bot
import uvicorn
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    ExtBot,
    CallbackQueryHandler, MessageHandler,
)


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

bots = {}
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update: {context.error}")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")
    for bot_name, config in BOT_CREDENTIALS.items():
        logger.info(f"Initializing bot: {bot_name}")
        bot = create_bot(config["token"])
        await bot.initialize()
        await bot.start()
        bots[bot_name] = bot
    await set_webhooks()
    # Add this line in the startup_event function, after creating each bot
    bot.add_error_handler(error_handler)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")
    for bot in bots.values():
        await bot.stop()
        await bot.shutdown()

@app.post("/webhook/{bot_name}")
async def handle_webhook(bot_name: str, request: Request):
    logger.info(f"Received webhook for bot: {bot_name}")
    if bot_name in bots:
        bot = bots[bot_name]
        update = await request.json()
        logger.debug(f"Received update for {bot_name}: {update}")
        try:
            await bot.process_update(Update.de_json(data=update, bot=bot.bot))
            logger.info(f"Processed update for {bot_name}")
        except Exception as e:
            logger.error(f"Error processing update for {bot_name}: {str(e)}")
        return {"status": "ok"}
    logger.warning(f"Bot not found: {bot_name}")
    return {"status": "error", "message": "Bot not found"}

async def set_webhooks():
    for bot_name, config in BOT_CREDENTIALS.items():
        webhook_url = f"https://your-domain.com{config['webhook_path']}"
        logger.info(f"Setting webhook for {bot_name} to {webhook_url}")
        await bots[bot_name].bot.set_webhook(webhook_url)

if __name__ == "__main__":
    logger.info("Starting the FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")