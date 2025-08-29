from utils import fetch_weather
import os

def get_weather(city):
    return fetch_weather(city, os.getenv("OPENWEATHER_API_KEY"))
