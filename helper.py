import requests
import streamlit as st
import os
WEATHER_API_KEY = st.secrets.get('WEATHER_API_KEY', os.getenv('WEATHER_API_KEY'))

if WEATHER_API_KEY:
    api_key = WEATHER_API_KEY

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