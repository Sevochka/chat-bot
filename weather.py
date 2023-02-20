import requests

api_key = "Ключ от API. Скрыт на GitHub."
base_url = "https://api.openweathermap.org/data/2.5/weather?units=metric&lang=ru&appid=" + api_key


def parse_weather(weather_json):
    print(weather_json)
    if weather_json["cod"] != "404":
        main = weather_json["main"]
        return {
            "temp": main["temp"],
            "pressure": main["pressure"],
            "humidity": main["humidity"],
            "description": weather_json["weather"][0]["description"],
            "city": weather_json["name"]
        }

    return None


def get_weather(city_name="Moscow"):
    complete_url = base_url + "&q=" + city_name
    response = requests.get(complete_url)
    weather = parse_weather(response.json())
    return weather


exported_functions = [get_weather]
