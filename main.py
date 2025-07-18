import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from numerology import get_luck_prediction
from database import save_number, save_chat
from together_ai import get_ai_response
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Share Your Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Welcome! Send me a phone number or message to get a lucky/unlucky prediction.")

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.effective_message.contact
    if contact and contact.phone_number:
        number = contact.phone_number
        save_number(number)
        prediction = get_luck_prediction(number)
        await update.message.reply_text(f"📞 Number: {number}
🔮 {prediction}")

async def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.from_user.id
    save_chat(user_id, text)
    # Extract numbers from bulk message
    import re
    numbers = re.findall(r"[+]?\d{9,15}", text)
    replies = []
    for num in numbers:
        save_number(num)
        result = get_luck_prediction(num)
        replies.append(f"📞 {num} → {result}")
    # AI response also
    ai_reply = get_ai_response(text)
    if replies:
        await update.message.reply_text("\n".join(replies))
    await update.message.reply_text(f"🤖 AI says: {ai_reply}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()