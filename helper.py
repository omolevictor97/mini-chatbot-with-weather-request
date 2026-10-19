import requests
import os
api_key = os.getenv('WEATHER_API_KEY', "33d915f1a1ea449374cf834794a3de91")
def get_weather(city:str):
    """The function takes city and returns the weather condition of the place"""
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")
    if weather_data.json()['cod'] == '404':
        return 'No city found'
    else:
        print(weather_data.json())
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])

    return f"""The weather in {city} is: {weather})
            The temperature in {city} is: {temp}ºF"""