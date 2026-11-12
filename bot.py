import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

WEB_APP_URL = "https://payoneerx2003-design.github.io/dogs-mini-app/"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        await context.bot.set_chat_menu_button(
            chat_id=user.id,
            menu_button=MenuButtonWebApp(text="🚀 Open App", web_app=WebAppInfo(url=WEB_APP_URL))
        )
    except Exception as e:
        print("Menu button error:", e)

    welcome_message = (
        f"Hello, {user.first_name}! 🐾\n\n"
        "Welcome to Claim Unlimited DOGS Free! ✨\n"
        "Click the button below or use the Menu button to launch the app."
    )
    
    keyboard = [
        [InlineKeyboardButton("🚀 Launch Mini App", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

if __name__ == '__main__':
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()

    TOKEN = "9009992955:AAE8RKaxD5SJK4Q01ay7s3-dsZYfSsFTbKU"
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Bot is running on cloud...")
    application.run_polling()
  
