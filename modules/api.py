import requests
import aiohttp
import asyncio
import time
from geopy.geocoders import Nominatim

main_api = "7ed0f20acb414f6cac5191700230212"
city_data = {}
locator = Nominatim(user_agent = "me")

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