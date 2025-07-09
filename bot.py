import os
import json
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загрузка кодов ошибок из файла
with open("obd2_errors.json", "r", encoding="utf-8") as f:
    error_codes = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь /code <код ошибки> или /launch_manual для получения PDF мануала.")

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи код ошибки: /code P0171")
        return

    code = context.args[0].upper()
    data = error_codes.get(code)
    if data:
        reply = f"🔧 Код: {code}\nПричина: {data['reason']}\nРешение: {data['solution']}"
    else:
        reply = "Код ошибки не найден в базе."
    await update.message.reply_text(reply)

async def launch_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("launch_manual.pdf", "rb") as f:
        await update.message.reply_document(InputFile(f, filename="launch_manual.pdf"))

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", code))
    app.add_handler(CommandHandler("launch_manual", launch_manual))
    print("✅ Бот запущен...")
    app.run_polling()
