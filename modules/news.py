from utils import fetch_news
import os

def get_news():
    return fetch_news(os.getenv("NEWS_API_KEY"))
