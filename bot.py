import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import asyncio
from io import BytesIO
from gtts import gTTS
import random
import html

# ------------------------- Load environment -------------------------
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")  # HuggingFace for image generation

# Configure free Gemini model
genai.configure(api_key=GEMINI_API_KEY)

# ------------------------- Fun / Trivia -------------------------
def get_fun_fact():
    try:
        data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        return data['text']
    except:
        return "Couldn't fetch fun fact."

user_scores = {}
def get_trivia_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    data = requests.get(url).json()
    q_data = data["results"][0]
    question = html.unescape(q_data["question"])
    correct = html.unescape(q_data["correct_answer"])
    options = [html.unescape(opt) for opt in q_data["incorrect_answers"]] + [correct]
    random.shuffle(options)
    return {"question": question, "options": options, "correct": correct}

# ------------------------- Media -------------------------
def generate_image(prompt):
    url = "https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return BytesIO(response.content)
    return None

def text_to_speech(text):
    tts = gTTS(text)
    path = "speech.mp3"
    tts.save(path)
    return path

# ------------------------- Commands -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 Chat", callback_data="chat")],
        [InlineKeyboardButton("🌦 Weather", callback_data="weather")],
        [InlineKeyboardButton("📰 News", callback_data="news")],
        [InlineKeyboardButton("⏰ Reminders", callback_data="remind")],
        [InlineKeyboardButton("🎉 Fun Fact", callback_data="fun")],
        [InlineKeyboardButton("❓ Trivia", callback_data="trivia")],
        [InlineKeyboardButton("🖼 AI Image", callback_data="image")],
        [InlineKeyboardButton("🔊 TTS", callback_data="tts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to Ryzex AI v4\nChoose an option:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
🤖 *Ryzex AI Commands*:
/chat <message> → Ask AI
/weather <city> → Weather updates
/news → Tech news
/remind <minutes> <message> → Reminders
/fun → Fun fact
/trivia → Trivia game
/image <prompt> → AI generated image
/say <message> → Text-to-speech
"""
    await update.message.reply_text(commands, parse_mode="Markdown")

# ------------------------- Callback Buttons -------------------------
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "chat":
        await query.message.reply_text("💬 Type /chat <your message> to ask AI anything.")
    elif data == "weather":
        await query.message.reply_text("🌦 Type /weather <city> to get weather updates.")
    elif data == "news":
        await query.message.reply_text("📰 Type /news for top tech news.")
    elif data == "remind":
        await query.message.reply_text("⏰ Type /remind <minutes> <message> to set a reminder.")
    elif data == "fun":
        await query.message.reply_text(f"🎉 Fun Fact:\n{get_fun_fact()}")
    elif data == "trivia":
        q = get_trivia_question()
        text = f"❓ Trivia:\n{q['question']}\nOptions: {', '.join(q['options'])}"
        await query.message.reply_text(text)
    elif data == "image":
        await query.message.reply_text("🖼 Type /image <prompt> to generate an AI image.")
    elif data == "tts":
        await query.message.reply_text("🔊 Type /say <message> for text-to-speech.")

# ------------------------- Chat / AI -------------------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("❌ Provide a message!")
        return
    try:
        model = genai.GenerativeModel("gemini-1.3-preview")  # FREE Gemini
        resp = model.generate_content(query)
        await update.message.reply_text(f"🤖 AI says:\n{resp.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# ------------------------- Weather -------------------------
async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args)
    if not city:
        await update.message.reply_text("❌ Provide a city name!")
        return
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        if data["cod"] != 200:
            await update.message.reply_text("⚠️ City not found!")
            return
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        await update.message.reply_text(f"🌦 Weather in {city}: {desc}, 🌡 {temp}°C")
    except:
        await update.message.reply_text("⚠️ Error fetching weather!")

# ------------------------- News -------------------------
async def news_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={NEWS_API_KEY}"
        data = requests.get(url).json()
        articles = data["articles"][:5]
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

# ------------------------- AI Image -------------------------
async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("❌ Provide a prompt!")
        return
    await update.message.reply_text("🎨 Generating image...")
    img = generate_image(prompt)
    if img:
        await update.message.reply_photo(photo=img)
    else:
        await update.message.reply_text("⚠️ Could not generate image.")

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

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chat", chat))
    app.add_handler(CommandHandler("weather", weather_cmd))
    app.add_handler(CommandHandler("news", news_cmd))
    app.add_handler(CommandHandler("remind", remind_cmd))
    app.add_handler(CommandHandler("image", image_cmd))
    app.add_handler(CommandHandler("say", say_cmd))

    # Callback buttons
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("🚀 Ryzex AI Assistant v4 running...")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(run_bot())
