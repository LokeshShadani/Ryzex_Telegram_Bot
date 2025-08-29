import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import asyncio
import html
import random
from gtts import gTTS

# ------------------------- Load environment -------------------------
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ------------------------- Configure Gemini -------------------------
genai.configure(api_key=GEMINI_API_KEY)

# ------------------------- Fun / Trivia -------------------------
def get_fun_fact():
    try:
        data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        return data['text']
    except:
        return "Couldn't fetch a fun fact."

def get_trivia_question():
    try:
        url = "https://opentdb.com/api.php?amount=1&type=multiple"
        data = requests.get(url).json()
        q_data = data["results"][0]
        question = html.unescape(q_data["question"])
        correct = html.unescape(q_data["correct_answer"])
        options = [html.unescape(opt) for opt in q_data["incorrect_answers"]] + [correct]
        random.shuffle(options)
        return {"question": question, "options": options, "correct": correct}
    except:
        return {"question": "Trivia not available", "options": [], "correct": ""}

# ------------------------- Media (TTS) -------------------------
def text_to_speech(text):
    tts = gTTS(text)
    path = "speech.mp3"
    tts.save(path)
    return path

# ------------------------- Bot Commands -------------------------
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 Chat", callback_data="chat")],
        [InlineKeyboardButton("🌦 Weather", callback_data="weather")],
        [InlineKeyboardButton("📰 News", callback_data="news")],
        [InlineKeyboardButton("⏰ Reminders", callback_data="remind")],
        [InlineKeyboardButton("🎉 Fun Fact", callback_data="fun")],
        [InlineKeyboardButton("❓ Trivia", callback_data="trivia")],
        [InlineKeyboardButton("🔊 TTS", callback_data="tts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to Ryzex AI\nChoose an option:",
        reply_markup=reply_markup
    )

# Auto-welcome when user sends any text
users_started = set()
async def auto_start_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users_started:
        users_started.add(user_id)
        await send_welcome(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
🤖 *Ryzex AI Commands*:
/chat <message> → Ask AI
/weather <city> → Weather updates
/news → Tech news
/remind <minutes> <message> → Reminders
/fun → Fun fact
/trivia → Trivia game
/say <message> → Text-to-speech
"""
    await update.message.reply_text(commands, parse_mode="Markdown")

# ------------------------- Callback Buttons -------------------------
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    try:
        await query.answer()
    except:
        pass

    data = query.data
    if data == "chat":
        await query.message.reply_text("💬 Type /chat <your message> to ask AI anything.")
    elif data == "weather":
        await query.message.reply_text("🌦 Type /weather <city> to get live weather updates.")
    elif data == "news":
        await query.message.reply_text("📰 Type /news to see top tech news.")
    elif data == "remind":
        await query.message.reply_text("⏰ Type /remind <minutes> <message> to set a reminder.")
    elif data == "fun":
        await query.message.reply_text(f"🎉 Fun Fact:\n{get_fun_fact()}")
    elif data == "trivia":
        q = get_trivia_question()
        text = f"❓ Trivia:\n{q['question']}\nOptions: {', '.join(q['options'])}"
        await query.message.reply_text(text)
    elif data == "tts":
        await query.message.reply_text("🔊 Type /say <message> for text-to-speech.")

# ------------------------- AI Chat -------------------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("❌ Provide a message!")
        return
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")  # Using Gemini 2.5 Flash model
        resp = model.generate_content(query)
        await update.message.reply_text(f"🤖 AI says:\n{resp.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Gemini API error: {e}")

# ------------------------- Weather -------------------------
async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args)
    if not city:
        await update.message.reply_text("❌ Provide a city name!")
        return
    try:
        # First try City + Country code
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        
        if data.get("cod") != 200:
            # Retry just city name
            city_name = city.split(",")[0]
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
            data = requests.get(url).json()
            
        if data.get("cod") != 200:
            await update.message.reply_text(f"⚠️ City '{city}' not found. Try 'City,CountryCode'")
            return

        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        await update.message.reply_text(f"🌦 Weather in {city}: {desc}, 🌡 {temp}°C")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error fetching weather: {e}")

# ------------------------- News -------------------------
async def news_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={NEWS_API_KEY}"
        data = requests.get(url).json()
        articles = data.get("articles", [])[:5]
        headlines = "\n\n".join([f"📰 {a['title']} ({a['source']['name']})" for a in articles])
        await update.message.reply_text(f"🔥 Top Tech News:\n{headlines}")
    except:
        await update.message.reply_text("⚠️ Could not fetch news!")

# ------------------------- Reminders -------------------------
async def remind_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = int(context.args[0])
        message = " ".join(context.args[1:])
        await update.message.reply_text(f"✅ Reminder set for {minutes} min!")
        await asyncio.sleep(minutes*60)
        await update.message.reply_text(f"⏰ Reminder: {message}")
    except:
        await update.message.reply_text("⚠️ Usage: /remind <minutes> <message>")

# ------------------------- TTS -------------------------
async def say_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("❌ Provide text to speak.")
        return
    path = text_to_speech(text)
    with open(path, "rb") as f:
        await update.message.reply_audio(f)
    os.remove(path)

# ------------------------- Run Bot -------------------------
def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", send_welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_start_message))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chat", chat))
    app.add_handler(CommandHandler("weather", weather_cmd))
    app.add_handler(CommandHandler("news", news_cmd))
    app.add_handler(CommandHandler("remind", remind_cmd))
    app.add_handler(CommandHandler("fun", lambda u,c: u.message.reply_text(get_fun_fact())))
    app.add_handler(CommandHandler("trivia", lambda u,c: u.message.reply_text(str(get_trivia_question()))))
    app.add_handler(CommandHandler("say", say_cmd))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 Ryzex AI Assistant running...")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(run_bot())
