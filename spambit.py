import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = '7736727214:AAF8ETLY8DoSFztqCAwqU9C1exfcRM8X6UQ'
WEBHOOK_URL = 'https://yourdomain.com/webhook'  # Change this to your actual webhook URL

shayari_list = [
    "Mohabbat karna har kisi ke bas ki baat nahi...",
    "Tere bina jee na paayenge hum...",
    "Dil se nikli har dua mein tu hai...",
    "Khamoshi bhi kabhi kabhi izhaar hoti hai...",
    "Tera chehra hai aaina, har roop mein tu yaad aata hai...",
    "Waqt ke saath sab kuch badal jaata hai, bas yaadein wahi rehti hain...",
    "Jo dil se diya jaaye, woh shayari hoti hai...",
    "Aaj phir dil ne ek tamana ki, tu saamne ho aur baat purani ho..."
]

abuse_list = [
    "Oye ullu ke patthe!",
    "Nikal pehli fursat mein!",
    "Aree chhoti bacchi ho kya?",
    "Tera baap aaya kya?",
    "Tumse na ho payega!",
    "Kya chaman banaya hai yaar tune!",
    "Abe oye, tumse na ho paayega!",
    "Abe gadhedi ke!",
    "O bhai maro mujhe maro!"
]

user_ids = set()

app = Flask(__name__)

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ids.add(update.effective_user.id)
    await update.message.reply_text("Welcome! Use /spam, /raid, /shayari or /broadcast.")

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /spam <count> <message>")
        return

    try:
        count = int(args[0])
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return

    count = min(count, 10)
    msg = ' '.join(args[1:])
    for _ in range(count):
        await update.message.reply_text(msg)

async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for _ in range(3):
        await update.message.reply_text(random.choice(shayari_list))
        await update.message.reply_text(random.choice(abuse_list))

async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_line = ' '.join(context.args)
    if user_line:
        random_line = random.choice(shayari_list)
        full_text = f"{user_line},\n{random_line}"
        await update.message.reply_text(full_text)
    else:
        await update.message.reply_text(random.choice(shayari_list))

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        msg = ' '.join(args)
        for uid in user_ids:
            try:
                await context.bot.send_message(chat_id=uid, text=f"[Broadcast]\n{msg}")
            except Exception as e:
                print(f"Could not send to {uid}: {e}")
        await update.message.reply_text("Broadcast sent.")
    else:
        await update.message.reply_text("Usage: /broadcast <message>")

@app.route(f'/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    application.update_queue.put(update)
    return "OK"

def main():
    # New Application builder pattern (v20+)
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spam", spam))
    application.add_handler(CommandHandler("raid", raid))
    application.add_handler(CommandHandler("shayari", shayari))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Set up the webhook
    application.bot.set_webhook(WEBHOOK_URL)

    # Run Flask app
    app.run(host='0.0.0.0', port=5000)  # Listen on port 5000

if __name__ == '__main__':
    main()
