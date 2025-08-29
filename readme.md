# 🤖 Ryzex AI Assistant

![Last Commit](https://img.shields.io/github/last-commit/LokeshShadani/Ryzex_Telegram_Bot?color=blue&style=for-the-badge)
![Repo Size](https://img.shields.io/github/repo-size/LokeshShadani/Ryzex_Telegram_Bot?color=green&style=for-the-badge)
![Open Issues](https://img.shields.io/github/issues/LokeshShadani/Ryzex_Telegram_Bot?color=red&style=for-the-badge)
![Stars](https://img.shields.io/github/stars/LokeshShadani/Ryzex_Telegram_Bot?color=yellow&style=for-the-badge)
![Python Version](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge)
![License](https://img.shields.io/github/license/LokeshShadani/Ryzex_Telegram_Bot?color=purple&style=for-the-badge)
![Latest Release](https://img.shields.io/github/v/release/LokeshShadani/Ryzex_Telegram_Bot?color=orange&style=for-the-badge)

---

## 🚀 Overview

**Ryzex AI Assistant** is an interactive Telegram bot designed to help users stay informed, entertained, and productive. It features AI chat, hyperlocal weather updates, tech news, reminders, and fun facts. Inline buttons and instant greetings provide a seamless user experience.

---

## 🛠️ Technologies Used

- **Bot Framework**: Python (python-telegram-bot v20.7)  
- **AI Model**: Gemini Flash AI  
- **Weather API**: Ambee Weather API  
- **News API**: NewsAPI.org  
- **Utilities**: requests, python-dotenv

---

## 📁 Project Structure

RyzexAI/
├── bot.py # Main Telegram bot script
├── .env # Environment variables
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── assets/ # Optional assets like images/icons

yaml
Copy code

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/lokesh/RyzexAI.git
cd RyzexAI

# Create virtual environment
python -m venv venv
# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
📌 Bot Commands & Features
Feature	Command	Status	Description
AI Chat	/chat <message>	✅ Active	Ask AI anything and get intelligent responses using Gemini Flash.
Weather Updates	/weather <city>	✅ Active	Get hyperlocal weather including temperature, humidity, wind speed using Ambee API.
Tech News	/news	✅ Active	Latest AI & tech news headlines from NewsAPI.
Reminders	/remind <minutes> <message>	✅ Active	Schedule personal reminders.
Fun Facts	/fun	✅ Active	Get a random fun fact.
Interactive Buttons	Inline	✅ Active	Navigate the bot without typing commands.
Instant Welcome	Auto	✅ Active	Bot greets new users automatically.

🧪 Status & Development
Feature	Status
AI Chat	✅ Active
Weather Updates	✅ Active
Tech News	✅ Active
Reminders	✅ Active
Fun Facts	✅ Active
Interactive Buttons	✅ Active
Instant Welcome	✅ Active

🤝 Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For major changes, open an issue first to discuss your ideas.

📄 License
This project is licensed under the MIT License.
