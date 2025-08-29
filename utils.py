import requests

def fetch_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    if data.get("cod") != 200:
        return None
    return f"🌦 Weather in {city}: {data['weather'][0]['description']}, 🌡 {data['main']['temp']}°C"

def fetch_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={api_key}"
    data = requests.get(url).json()
    articles = data.get("articles", [])[:5]
    headlines = "\n\n".join([f"📰 {a['title']} ({a['source']['name']})" for a in articles])
    return f"🔥 Top Tech News:\n\n{headlines}"

def fetch_fun_fact():
    try:
        data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        return data['text']
    except:
        return "⚠️ Couldn't fetch fun fact right now!"
