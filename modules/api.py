import requests
import aiohttp
import asyncio
import calendar
from geopy.geocoders import Nominatim
from deep_translator.google import GoogleTranslator
from timezonefinder.timezonefinder import TimezoneFinder
from datetime import datetime
from pytz import timezone as pytz_tz

main_api = "7ed0f20acb414f6cac5191700230212"
city_data = {}
locator = Nominatim(user_agent = "me")
time_locator = Nominatim(user_agent = "also_me")

def get_api_data(city):
    location = locator.geocode(city)
    with requests.Session() as session:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={main_api}&q={location.latitude},{location.longitude}&days=2"
        response = session.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Unknown error occured while handling request")
        return "Error: API_RESPONSE_CODE"
    
async def async_get_api_data(city_list: list = ["London"]):
    global city_data
    city_data = {}
    try:
        async with aiohttp.ClientSession() as session:
            for city_name in city_list:
                location = locator.geocode(city_name)
                try:
                    async with session.get(f"http://api.weatherapi.com/v1/forecast.json?key={main_api}&q={location.latitude},{location.longitude}&days=2") as response:
                        if response.status == 200:
                            data = await response.json()
                            city_data.update({city_name: data})
                        else:
                            print("Unknown error occured while handling asynchronous request")
                            city_data.update({"Error": "API_ASYNC_RESPONSE_CODE"})
                except:
                    print("Error in api: No such city.")
                    city_data.update({"Error": "API_ASYNC_NO_SUCH_CITY"})
    except:
        print("Error: Unknown error at creating session.")
        city_data.update({"Error": "API_ASYNC_SESSION"})
    return city_data

def get_time_by_tz(city: str = "London"):
    translator = GoogleTranslator(target = "uk")
    timezone_searcher = TimezoneFinder()

    coors = time_locator.geocode(city)
    timezone = timezone_searcher.timezone_at(lat = coors.latitude, lng = coors.longitude)
    timezone = pytz_tz(timezone)

    time_somewhere = datetime.now(timezone)
    current_time_somewhere = time_somewhere.strftime("%H:%M,%D,%W").split(",")

    return {
            "time": current_time_somewhere[0],
            "date": current_time_somewhere[1],
            "week_day": translator.translate(calendar.day_name[time_somewhere.today().weekday()])
            }