# File to make all API-connected operations

import json

import requests

city = input("Введите свой город:  ")

GEOCODER_API_KEY = "5fd2cc9c-5767-4584-84b9-2842f64f7fc5"
WEATHER_API_KEY = "82d7f11f-c897-46ab-bc28-c2445ffd9e7d"
# TODO: Relocate all vital constants to the dot-env file

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
geocoder_request = geocoder_base + f"&geocode={city}&lang=ru_RU&format=json"
response_city = requests.get(geocoder_request)
if not response_city:
    response_city.raise_for_status()
city_response = json.loads(response_city.text)
toponym = city_response["response"]["GeoObjectCollection"]["featureMember"][0][
    "GeoObject"
]
coords = toponym["Point"]["pos"].split()
weather_request = weather_base + f"?lat={coords[1]}&lon={coords[0]}"
response_weather = requests.get(weather_request, headers=weather_headers)
if not response_weather:
    response_weather.raise_for_status()
json_weather_response = json.loads(response_weather.text)
# Getting our variables ready
now = json_weather_response["fact"]

temp = now["temp"]
like = now["feels_like"]
cond = CONDITIONS[now["condition"]]
print(
    f"Сейчас в городе {city} {temp} градусов, ощущается как {like} градусов."
    f" На улице {cond}."
)
