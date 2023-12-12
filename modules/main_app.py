import customtkinter as ctk
import asyncio
import time
import os
import urllib.request
from aiohttp import ClientSession
from deep_translator.google import GoogleTranslator
from PIL import Image
import modules.database as data
import modules.find_path as fp
import modules.api as api

start_city = None
city, api_data = "Дніпро", ""
main_app_existing = False
info_about_other_places = {}
api_city_data = {}

def activate_window(user_data: dict, data_reg_window_fun, database_funcs: dict = {"func_name": "func"}):
    global city, api_data, main_app_existing, info_about_other_places, start_city, api_city_data
    
    api_city_data = {}
    main_app_existing = True
    if type(user_data) != str:
        city = user_data["City"]
        user_name = f'{user_data["Name"]} {user_data["Surname"]}'
    else:
        city = "Київ"
        user_name = user_data
    app = ctk.CTkToplevel()
    app.geometry("1200x800")

    translator = GoogleTranslator(target = "uk")
    TRANSPARENT = app._apply_appearance_mode(['#f2f2f2','#000001'])
    app.attributes("-transparentcolor", TRANSPARENT)
    app.config(background = TRANSPARENT)
    app.overrideredirect(1)

    window = ctk.CTkFrame(
        master = app,
        width = 1200, height = 800, corner_radius = 20,
        border_width = 5, border_color = "#096c82", fg_color = "#5da7b1",
        bg_color = TRANSPARENT
    )
    side_panel = ctk.CTkScrollableFrame(
        master = window,
        width = 281, height = 800, border_width = 3,
        border_color = "#096c82", fg_color = "#096c82",
        corner_radius = 20, bg_color = TRANSPARENT, scrollbar_button_color = "#096c82"
    )
    icon = ctk.CTkLabel(
        master = window,
        width = 165, height = 165, fg_color = "transparent",
        text = " "
    )
    delete_city = ctk.CTkButton(master = window,
                                width = 50, height = 50, fg_color = "transparent",
                                image = ctk.CTkImage(Image.open(fp.search_path("images\\icons\\trashbin_icon.png")), size = (50, 50)), text = " ", command = lambda: 1 + 1, hover_color = "#5da7b1")
                                
    def close_command():
        global main_app_existing
        main_app_existing = False
        app.destroy()
    close_window_button = ctk.CTkButton(
                                        master = window, width = 50, height = 50, 
                                        fg_color = "#096c82", border_width = 0, hover_color = "#bf0000",
                                        text = "X", command = close_command, background_corner_colors = ["#096c82", TRANSPARENT, "#096c82", "#5da7b1"]
                                        )
    # search field section
    main_search_background = ctk.CTkFrame(master = window, width = 216, height = 42, corner_radius = 20,
                                        fg_color = "#096c82", border_width = 3, border_color = "#dbdbdb"
                                        )
    search_entry_field = ctk.CTkEntry(
                                        master = main_search_background, width = 130, height = 35,
                                        fg_color = "transparent", placeholder_text = "пошук", 
                                        font = ctk.CTkFont('Roboto Slab', 16), text_color = "#dbdbdb", 
                                        placeholder_text_color = "#dbdbdb", border_width = 0
    )
    search_button = ctk.CTkButton(master = main_search_background, 
                                  width = 27, height = 27, fg_color = "transparent",
                                  hover_color = main_search_background.cget("fg_color"), command = lambda: 1 + 1,
                                  text = " ", image = ctk.CTkImage(Image.open(fp.search_path("images\\icons\\search_icon.png")), size = (27, 27)))

    # user account data section
    def enter_acc():
        print('enter reg')
        data_reg_window_fun()
        print("not enter reg")
    user_account_enter = ctk.CTkButton(master = window,
                                       width = 50, height = 60, fg_color = "transparent",
                                       command = enter_acc, text = " ", hover_color = "#096c82",
                                       image = ctk.CTkImage(Image.open(fp.search_path("images\\icons\\user_icon.png")), size = (50, 50)),
                                       font = ctk.CTkFont('Inter', 20, "bold")
                                       )

    info_current_pos = {}

    create_text = {"current_position": ["Поточна позиція", 35, "Roboto Slab"], 
                "city": ["Город", 22, "Roboto Slab"], 
                "temperature": ["Температура", 80, "Inter"],
                "main_weather":["Погода", 30, "Roboto Slab"],
                "sub_weather": ["Суб-погода", 16, "Roboto Slab"],
                "max_min_temperature": ["Максимальная и минимальная температура", 30, "Inter"]}

    for name in create_text:
        info_current_pos.update({name: ctk.CTkLabel(
                                                    master = window, 
                                                    width = 0, height = 0, fg_color = "transparent",
                                                    text = create_text[name][0], font = ctk.CTkFont(create_text[name][2], create_text[name][1])

        )})
    # 
    current_time = {}

    def get_main_weather(full_weather):
        full_weather = translator.translate(full_weather).split(" ")
        if len(full_weather) > 1:
            full_weather = full_weather[-1]
            full_weather = f"{full_weather[0].capitalize()}{full_weather[1:]}"
        return full_weather

    create_text = {
        "week_day": ["Вторник", 18, "Roboto Slab", "normal"],
        "date": ["27.13.22", 40, "Roboto Slab", "normal"],
        "current_time": ["12:34", 30, "Roboto Slab", "bold"]
    }

    for key in create_text:
        current_time.update({key: ctk.CTkLabel(
            master = window, width = 0, height = 0,
            fg_color = "transparent", text = create_text[key][0],
            font = ctk.CTkFont(create_text[key][2], create_text[key][1], create_text[key][3]),
        )})


    current_weather_table = ctk.CTkFrame(
        master = window, width = 818, height = 240, 
        corner_radius = 20, border_width = 5, fg_color = "transparent",
        border_color = "#dbdbdb"
        )
    a_line = ctk.CTkFrame(
        master = window, width = 818, height = 2, 
        border_width = 1, fg_color = "#dbdbdb",
        border_color = "#dbdbdb"
    )

    hour_forecast_tables = {}
    api_data = 0

    def update_hour_forecast():
        global api_data
        
        api_data = api.get_api_data(city)
        forecast_nine_hours = {}
        print(time.strftime("%H"))
        hours = api_data["forecast"]["forecastday"][0]["hour"][int(time.strftime("%H")):]
        if len(hours) < 9:
            hours.extend(api_data["forecast"]["forecastday"][0]["hour"][:9 - len(hours)])
        # print(hours)
        for hour_forecast in hours:
            hour = hour_forecast["time"].split(" ")[1]
            if len(forecast_nine_hours) < 9:
                forecast_nine_hours.update({hour: [fp.search_path(f"images\\icons\\{hour_forecast['condition']['text']}_icon.png"), f"{round(hour_forecast['temp_c'])}°",
                                                    hour_forecast["condition"]]})
        
        if len(hour_forecast_tables) != 0:
            forecast_nine_hours_keys = list(forecast_nine_hours)
            hour_forecast_tables_keys = list(hour_forecast_tables)
            for count in range(9):
                hour = forecast_nine_hours_keys[count]
                # print(hour_forecast_tables_keys, count)
                part = hour_forecast_tables_keys[count]
                hour_forecast_tables[part][0].configure(True, text = hour)

                if not os.path.exists(forecast_nine_hours[hour][0]):
                    os.chdir(fp.search_path("images\\icons"))
                    icon_name = forecast_nine_hours[hour][2]["text"]
                    # print(icon_name)
                    urllib.request.urlretrieve(f"http:{forecast_nine_hours[hour][2]['icon']}", f"{icon_name}_icon.png")
                    os.chdir(__file__ + "/..")

                hour_forecast_tables[part][1].configure(True, image = ctk.CTkImage(Image.open(forecast_nine_hours[hour][0]), size = (54, 50)))
                hour_forecast_tables[part][2].configure(True, text = forecast_nine_hours[hour][1])
        else:
            for hour in forecast_nine_hours:
                
                if not os.path.exists(forecast_nine_hours[hour][0]):
                    os.chdir(fp.search_path("images\\icons"))
                    icon_name = forecast_nine_hours[hour][2]["text"]
                    # print(icon_name)
                    urllib.request.urlretrieve(f"http:{forecast_nine_hours[hour][2]['icon']}", f"{icon_name}_icon.png")
                    os.chdir(__file__ + "/..")
                hour_forecast_tables.update({f"{10 + len(hour_forecast_tables) * 90},55": [ctk.CTkLabel(master = current_weather_table, width = 0, height = 31,
                                                                                                        fg_color = "transparent", text = hour, font = ("Roboto Slab", 20)),
                                                                                            ctk.CTkLabel(master = current_weather_table, width = 54, height = 50,
                                                                                                        image = ctk.CTkImage(Image.open(forecast_nine_hours[hour][0]), size = (54, 50)),
                                                                                                        fg_color = "transparent", text = " "),
                                                                                            ctk.CTkLabel(master = current_weather_table, width = 0, height = 31,
                                                                                                        fg_color = "transparent", text = forecast_nine_hours[hour][1], 
                                                                                                        font = ctk.CTkFont("Roboto Slab", 30, "bold"))]})

    # "city": ["Город", 22 ,"Roboto Slab"], 
    # "temperature": ["Температура", 80 ,"Inter"],
    # "main_weather":["Погода", 30,"Roboto Slab"],
    # "sub_weather": ["Суб-погода", 16,"Roboto Slab"],
    # "max_min_temperature": ["Максимальная и минимальная температура", 30,"Inter"]}

    async def add_api_data(city_name: str = "London"):
        global api_city_data 
        api_city_data.update(await api.async_get_api_data([city_name]))
        # print(await api.async_get_api_data([city_name]))

    def update_city_data(what = "test"):
        print(f"bind succeful: {what}")
        global city
        city = search_entry_field.get()
        asyncio.run(add_api_data(city))
        asyncio.run(add_other_city_data(city, True))
        update_info_about_current_place()
        update_hour_forecast()

    def update_time():
        current_time["current_time"].configure(True, text = f"{time.strftime('%H')}:{time.strftime('%M')}")
        current_time["date"].configure(True, text = f"{time.strftime('%d')}.{time.strftime('%m')}.{time.strftime('%Y')}")
        app.after(60000, update_time)

    def update_info_about_current_place():
        api_data = api.get_api_data(city)
        if city != start_city:
            info_current_pos["current_position"].configure(True, text = city)
            info_current_pos["city"].configure(True, text = " ")
        else:
            info_current_pos["current_position"].configure(True, text = "Поточна позиція")
            info_current_pos["city"].configure(True, text = city)

        temp = f'{round(api_data["current"]["temp_c"])}°'
        info_current_pos["temperature"].configure(True, text = temp)
        weather_raw = api_data["current"]["condition"]["text"]
        weather = translator.translate(weather_raw)
        info_current_pos["main_weather"].configure(True, text = get_main_weather(weather_raw))
        if len(weather.split(' ')) > 1:
            info_current_pos["sub_weather"].configure(True, text = weather)
        else:
            info_current_pos["sub_weather"].configure(True, text = " ")
        day_data = api_data["forecast"]["forecastday"][0]["day"]
        info_current_pos["max_min_temperature"].configure(True, text = f"↑{round(day_data['maxtemp_c'])}° ↓{round(day_data['mintemp_c'])}°")
        icon.configure(True, image = ctk.CTkImage(Image.open(fp.search_path(f"images\\icons\\{weather_raw}_icon.png")), size = (165, 165)))
        update_time()
        
    info_about_other_places = {}

    def config_active(color = "#096c82"):
        info_about_other_places["active"]["main"].configure(True, fg_color = color)
        info_about_other_places["active"]["main"].configure(True, hover_color = color)
        for name in info_about_other_places["active"]["elements"]:
            info_about_other_places["active"]["elements"][name][0].configure(True, fg_color = color)
            info_about_other_places["active"]["elements"][name][0].configure(True, bg_color = color) 
            
    def update_city_data_by_button(city_name: str = "London"):
        global city
        city = city_name
        update_info_about_current_place()
        update_hour_forecast()
        config_active()
        info = info_about_other_places["active"]
        info_about_other_places.update({info["city"]: info})
        info_about_other_places.update({"active": info_about_other_places[city_name]})
        config_active("#5da7b1")

    async def add_other_city_data(
            city_name: str = "London", 
            add_in_database: bool = False, 
            city_data: list = ["London"]
            ):
        global info_about_other_places, start_city, api_city_data
        city_data = database_funcs["read"](_index_data = 5)["data"]
        print(f"pre if: \nnot in: {city_name not in city_data}\ncity_data = {city_data}")
        if city_name not in city_data or add_in_database == False:
            print("after if")
            if add_in_database:
                database_funcs["edit"](data = {"City_list": f"{city_data},{city_name}"})
            api_data = api_city_data[city_name]
            print(api_data)
            main_bg = ctk.CTkButton(master = side_panel,
                                    width = 236, height = 101, text = " ",
                                    fg_color = "#096c82", 
                                    border_color = "#dbdbdb", border_width = 2,
                                    corner_radius = 20, hover_color = "#096c82",
                                    command = lambda: update_city_data_by_button(city_name))
            min_max_t = api_data['forecast']['forecastday'][0]['day']
            if len(info_about_other_places) == 0:
                city_text = "Поточна позиція"
                time_text = translator.translate(api_data["location"]["name"])
                title = "active"
                main_bg.configure(True, fg_color = "#5da7b1")
                main_bg.configure(True, hover_color = "#5da7b1")
                start_city = city_name
            else:
                city_text =  translator.translate(api_data["location"]["name"])
                time_text = api_data["location"]["localtime"].split(" ")[1]
                title = city_name
            text_elements = {"city": [ctk.CTkLabel(master = main_bg, text = city_text, font = ("Roboto Slab", 16), fg_color = "transparent"), (14, 8)],
                            "time": [ctk.CTkLabel(master = main_bg, text = time_text, font = ("Roboto Slab", 12), fg_color = "transparent"), (14, 33)],
                            "weather": [ctk.CTkLabel(master = main_bg, text = get_main_weather(api_data["current"]["condition"]["text"]), font = ("Roboto Slab", 12), text_color = "#dbdbdb", fg_color = "transparent"), (14, 62)],
                            "temp": [ctk.CTkLabel(master = main_bg, text = f"{round(api_data['current']['temp_c'])}°", font = ("Inter", 50), fg_color = "transparent"), (158, 12)],
                            "temp_nim_max": [ctk.CTkLabel(master = main_bg, text = f"макс.: {round(min_max_t['maxtemp_c'])}°, мін.: {round(min_max_t['mintemp_c'])}°", font = ("Inter", 12), fg_color = "transparent"), (122, 62)]}
            for el in text_elements:
                element = text_elements[el]
                element[0].place(x = element[1][0], y = element[1][1])
            main_bg.pack(pady = 16)
            print("Place other city " + city_name)
            info_about_other_places.update({title: {"main": main_bg, "city": city_name, "elements": text_elements, "coors": [19, 31 + len(info_about_other_places) * 133]}})

    async def read_city_list_data():
        global city, api_city_data
        city_data = database_funcs["read"](_index_data = 5)["data"]
        cities = city_data.split(",")
        api_city_data = await api.async_get_api_data(cities)
        for city_n in cities:
            print(f"New city: {city_n}")
            await add_other_city_data(city_name = city_n)
        
    def place_current_info():
        # center - 733
        # В этом списке указаны только значения у
        y_cors_list = [131, 177, 238, 294, 330, 370]
        keys = list(info_current_pos)
        for count in range(6):
            info_current_pos[keys[count]].place(x = 733, y = y_cors_list[count], anchor = ctk.CENTER)
        coordinat_y = [191, 227, 274]
        keys = list(current_time)
        
        for y in range(3):
            current_time[keys[y]].place(x = 1009, y = coordinat_y[y], anchor = "n")

    def place_hour_forecast():
        for hour in hour_forecast_tables:
            cors = hour.split(",")
            cors = [int(cors[0]), int(cors[1])]
            hour_forecast_tables[hour][0].place(x = cors[0] + 27, y = cors[1], anchor = "n")
            hour_forecast_tables[hour][1].place(x = cors[0], y = cors[1] + 49)
            hour_forecast_tables[hour][2].place(x = cors[0] + 27, y = cors[1] + 119, anchor = "n")
    
    def delete_new_city():
        global info_about_other_places
        if start_city != info_about_other_places["active"]["city"]:  
            info_about_other_places["active"]["main"].destroy()
            deleted_city = info_about_other_places["active"]["city"]
            cities = data.read_data_by_id(_index_data = 5)["data"].split(",")
            del info_about_other_places["active"]
            cities.remove(deleted_city)
            data.edit_data(data = {"City_list": ",".join(cities)})
            info_about_other_places.update({"active": info_about_other_places.pop(list(info_about_other_places)[0])})
            for city in info_about_other_places:
                info_about_other_places[city]["main"].configure(True, state = "hidden")
            for city in info_about_other_places:
                info_about_other_places[city]["main"].pack(pady = 16)  
            config_active()
    
    delete_city.configure(True, command = delete_new_city)
    # Редактирование всех элементов и задавание параметров
    search_entry_field.bind(command = update_city_data, sequence = '<Return>')
    search_button.configure(True, command = update_city_data)
    update_info_about_current_place()
    update_hour_forecast()
    user_account_enter.configure(True, text = user_name)
    user_account_enter.configure(True, width = 70 + 10 * len(user_name))
    # print(f"width in calculations = {70 + 10 * len(user_name_text.cget('text'))}\nreal width = {user_account_enter.cget('width')}\ntext and len = {user_name_text.cget('text')}, {len(user_name_text.cget('text'))}")

    # Размещение всех элементов окна

    main_search_background.place(x = 918, y = 31)
    search_entry_field.place(x = 65, y = 4)
    search_button.place(x = 14, y = 4)

    delete_city.place(x = 712, y = 730)
    close_window_button.place(x = 1200, y = 0, anchor = "ne")
    user_account_enter.place(x = 323, y = 24)
    window.place(x = 0, y = 0)
    side_panel.place(x = -2, y = -20)
    current_weather_table.place(x = 325, y = 430)
    icon.place(x = 388, y = 171)
    a_line.place(x = 325, y = 476)
    place_current_info()
    place_hour_forecast()
    asyncio.run(read_city_list_data())
    # app.mainloop()
    
        