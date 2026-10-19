import requests
import streamlit as st
import os
import urllib.parse
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

# New Tool: Generates an image and returns a dynamic markdown image URL

def generate_image(prompt: str) -> str:
    """
    Call this tool ONLY when the user explicitly asks to create, draw, generate, 
    or design an image, painting, photo, or visual artwork.
    """
    # Clean the prompt and convert space characters to an API friendly URL format
    encoded_prompt = urllib.parse.quote(prompt.strip())
    # Generate a free, dynamic image URL (Flux model variant)
    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&model=flux&enhance=true"
    
    # Return standard markdown image syntax so Streamlit natively parses it
    return f"Here is your generated image:\n\n![AI Image]({image_url})"