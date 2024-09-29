from settings import valid_key_ya

# city = {
#      "url_1": "Бийске",
#      "url_2": "Краснообске"
# }

base_url = "https://api.weather.yandex.ru/v2/informers?"
url_bs = "lat=52.5363900&lon=85.2072200"
url_ks = "lat=54.9198000&lon=82.9909000"
headers = {"X-Yandex-API-Key": valid_key_ya}

condition = {
     "clear": "ясно",
     "partly-cloudy": "малооблачно",
     "cloudy": "облачно с прояснениями",
     "overcast": "пасмурно",
     "light-rain": "небольшой дождь",
     "rain": "дождь",
     "heavy-rain": "сильный дождь",
     "showers": "ливень",
     "wet-snow": "дождь со снегом",
     "light-snow": "небольшой снег",
     "snow": "снег",
     "snow-showers": "снегопад",
     "hail": "град",
     "thunderstorm": "гроза",
     "thunderstorm-with-rain": "дождь с грозой",
     "thunderstorm-with-hail": "гроза с градом"
}


# Определение координат населенных пунктов https://dateandtime.info/ru/index.php#
