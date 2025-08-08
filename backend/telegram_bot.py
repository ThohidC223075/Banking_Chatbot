import toml
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from fetch_info import answer_query
from convert_query_to_english import clean_query

# Load Telegram token
secrets = toml.load("secrets.toml")
TELEGRAM_BOT_TOKEN = secrets["telegram"]["bot_token"]

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send me a question and I’ll try to answer it using my knowledge base."
    )

# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = clean_query(user_input)
        answer, _ = answer_query(response, user_input)  # We discard the sources here
        await update.message.reply_text(answer, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

# Run bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
