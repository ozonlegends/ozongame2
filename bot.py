import logging
import os
import threading
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from flask import Flask

# ===== НАСТРОЙКИ ИЗ ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# ===== ЛОГИ =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ===== TELEGRAM =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"Привет, {user.first_name if user else 'легенда'}!\n\n"
        "Это *OZON LEGENDS* — визуальная игра про прокачку персонажа и склада.\n"
        "Нажми кнопку ниже, чтобы открыть игру."
    )

    
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown",
    )

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("Telegram-бот запущен")
    app.run_polling()

# ===== WEB SERVER (для Render Web Service) =====
web_app = Flask(__name__)

@web_app.route("/")
def index():
    return "OZON LEGENDS bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

# ===== START =====
if __name__ == "__main__":
    # Flask в отдельном потоке, чтобы Render видел HTTP-сервис
    threading.Thread(target=run_web, daemon=True).start()

    # Telegram-бот в главном потоке (нужен event loop)
    run_bot()


