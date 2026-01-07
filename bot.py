import logging
import os
import threading

from flask import Flask

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ===== НАСТРОЙКИ ИЗ ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
# WEBAPP_URL не нужен для варианта A (открытие через Menu Button),
# но оставляю чтение, чтобы не ломать твою структуру:
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения Render")

# ===== ЛОГИ =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ===== TELEGRAM =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user and user.first_name else "легенда"

    text = (
        f"Привет, {name}!\n\n"
        "Это *OZON LEGENDS* — визуальная игра про прокачку персонажа и склада.\n\n"
        "Открывай игру через кнопку *Меню* внизу чата.\n"
    )

    
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
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
    port = int(os.environ.get("PORT", "10000"))
    web_app.run(host="0.0.0.0", port=port)

# ===== START =====
if __name__ == "__main__":
    # Flask в отдельном потоке, чтобы Render видел HTTP-сервис
    threading.Thread(target=run_web, daemon=True).start()

    # Telegram-бот в главном потоке
    run_bot()
