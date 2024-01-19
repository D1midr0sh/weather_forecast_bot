# File to make all API-connected operations

import json
import os

from dotenv import load_dotenv

import requests

load_dotenv()

GEOCODER_API_KEY = os.environ.get("GEOCODER_API_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

CONDITIONS = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "drizzle": "морось",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "moderate-rain": "умеренно сильный",
    "heavy-rain": "сильный дождь",
    "continuous-heavy-rain": "длительный сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "thunderstorm-with-hail": "гроза с градом",
}
DAY_PARTS = {
    "night": "ночью",
    "morning": "утром",
    "day": "днем",
    "evening": "вечером",
    "fact": "сейчас",
}

geocoder_base = "http://geocode-maps.yandex.ru/1.x/?apikey=" + GEOCODER_API_KEY
weather_base = "https://api.weather.yandex.ru/v2/informers"
weather_headers = {"X-Yandex-API-Key": WEATHER_API_KEY}
def get_city_coords(city):
    geocoder_request = geocoder_base + f"&geocode={city}&lang=ru_RU&format=json"
    response_city = requests.get(geocoder_request)
    if not response_city:
        response_city.raise_for_status()
    city_response = json.loads(response_city.text)
    toponym = city_response["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"
    ]
    coords = toponym["Point"]["pos"].split()
    return coords


def get_weather(city):
    coords = get_city_coords(city)
    weather_request = weather_base + f"?lat={coords[1]}&lon={coords[0]}"
    response_weather = requests.get(weather_request, headers=weather_headers)
    if not response_weather:
        response_weather.raise_for_status()
    json_weather_response = json.loads(response_weather.text)
    # Getting our variables ready
    now = json_weather_response["fact"]
    now["condition"] = CONDITIONS[now["condition"]]
    forecast = json_weather_response["forecast"]
    weather = dict()
    weather["now"] = now
    weather["forecast"] = []
    for part in forecast["parts"]:
        part["condition"] = CONDITIONS[part["condition"]]
        part["part_name"] = DAY_PARTS[part["part_name"]]
        weather["forecast"].append(part)
    weather["info"] = json_weather_response["info"]
    return weather


def get_message(city):
    weather = get_weather(city)
    message = "Привет!\n"
    message += f"В твоём городе сейчас {weather['now']['condition']}, "
    message += f"температура воздуха {weather['now']['temp']}, но"
    message += f" ощущается как {weather['now']['feels_like']}."
    for part in weather["forecast"]:
        message += f"\n\n{part['part_name'].capitalize()} обещают что будет {part['condition']} "
        message += f"и температура воздуха в среднем достигнет {part['temp_avg']} градусов."
    message += f"\n\n Подробнее о прогнозе: {weather['info']['url']}"
    return message


city = input("Введите свой город:  ")
print("\n" + get_message(city))