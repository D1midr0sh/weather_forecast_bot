# Погодный бот
## Актуальные функции
* Получение прогноза погоды на день при отправке названия города или какого-либо места
## Планируемые функции
* Возможность запланировать отправку прогноза на определённое время на каждый день
# Установка проекта
1. Установить все библиотеки из `requirements.txt` следующей командой:
```
pip install -r requirements.txt
```
2. Создать файл `.env` в директории проекта, и поместить в него следующие переменные:
  * GEOCODER_API_KEY - Ваш ключ от API Геокодера
  * WEATHER_API_KEY - Ваш ключ от API Яндекс Погоды
  * BOT_TOKEN - Ваш ключ от Telegram Bot API
  Ключи для API Геокодера и Яндекс Погоды можно получить [здесь](https://developer.tech.yandex.ru/services), а ключ для Telegram Bot API [здесь](https://t.me/BotFather).
3. Запустить проект в среде разработки или через консоль командой
```
python bot.py
```
