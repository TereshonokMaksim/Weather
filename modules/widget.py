import customtkinter as ctk
from PIL import Image
import urllib.request
from deep_translator import GoogleTranslator
import modules.find_path as f_path
import modules.api as api
import modules.main_app as main_app
import os, asyncio, time
import pynput

widget_launched = 0
weather_id, city, app, app_size, translator, move_click, mouse_coordinates, max_coordinates, blank_spase, definition_mouse_and_screen, last_click, weather_full = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def create_widget(data, data_reg_window_fun, database_functions: dict = {"func_name": "func"}):
    global weather_id, city, app, app_size, translator, move_click, mouse_coordinates, max_coordinates, blank_spase, definition_mouse_and_screen, last_click, weather_full, widget_launched
    widget_launched = 1
    translator = GoogleTranslator(source = "auto", target = "uk")
    weather_id = None
    city = data["City"]

    app_size = (350, 350)
    app = ctk.CTk(fg_color = "#072038")
    app.geometry(f"{app_size[0]}x{app_size[1]}+{app.winfo_screenwidth() // 2 - app_size[0] // 2}+{app.winfo_screenheight() // 2 - app_size[1] // 2}") 
    app.title("Weather")

    TEMP_FONT = ctk.CTkFont("Inter", size = 80)
    BIG_FONT = ctk.CTkFont("Inter", size = 60)
    STANDART_FONT = ctk.CTkFont("Roboto Slab", size = 30)
    SMALL_FONT = ctk.CTkFont("Roboto Slab", size = 20)
    STANDART_TEXT_COLOR = "#ffffff" 

    TRANSPARENT = app._apply_appearance_mode(['#f2f2f2','#000001'])
    app.attributes("-transparentcolor", TRANSPARENT)
    app.config(background = TRANSPARENT)
    background = ctk.CTkFrame(master = app, width = 350, height = 350, 
                            corner_radius = 20, border_width = 5, 
                            background_corner_colors = (None, None, None, None), bg_color = TRANSPARENT,
                            border_color = "#096c82", fg_color = "#5da7b1"
    ) 


    weather_icon = ctk.CTkLabel(
        master = background, width = 80, height = 80,
        text = " ", corner_radius = 0, fg_color = "transparent"
    )

    city_label = ctk.CTkLabel(
        master = background, width = 0, height = 30, 
        text = "Space", fg_color = "transparent",
        font = BIG_FONT, text_color = STANDART_TEXT_COLOR
    )

    temp_label = ctk.CTkLabel(
        master = background, width = 70, height = 70, 
        text = "0°C", fg_color = "transparent", 
        font = TEMP_FONT, text_color = STANDART_TEXT_COLOR
    )

    weather_text = ctk.CTkLabel(
        master = background, width = 0, height = 28, 
        text = "fallout", fg_color = "transparent", 
        font = STANDART_FONT, text_color = STANDART_TEXT_COLOR
    )

    weather_full_text = ctk.CTkLabel(
        master = background, width = 0, height = 28, 
        text = " in the form of nuclear bombs",
        fg_color = "transparent", font = SMALL_FONT, text_color = STANDART_TEXT_COLOR
    )

    min_max_temperature = ctk.CTkLabel(
        master = background, width = 0, height = 30, 
        text = "🠕SCGG(3)° 🠗-TREE(3)°", fg_color = "transparent",
        font = STANDART_FONT, text_color = STANDART_TEXT_COLOR
    )
    print(f_path.search_path(r"images\icons\reset_icon.png"))
    image = Image.open(f_path.search_path("images\\icons\\reset_icon.png"))
    print(image)
    button_image = ctk.CTkImage(image, size = (25, 25))
    print(button_image)
    reset_button = ctk.CTkButton(
        master = background, width = 25, height = 25,
        fg_color = "transparent", text = " ", command = lambda: 1 + 1,
        image = button_image
    )

    mouse_coordinates = [0, 0]
    move_click = False
    blank_space = 0#(app.winfo_width() - background.cget('width')) // 2
    print(f"{blank_space} \n({app.winfo_width()} - {background.cget('width')}) // 2")
    max_coordinates = (app.winfo_screenwidth() - app_size[0], app.winfo_screenheight() - 40 - app_size[1])
    print(max_coordinates)
    definition_mouse_and_screen = (0, 0)

    def check_move(x, y):
        if move_click:
            app_cors = [x + definition_mouse_and_screen[0], y + definition_mouse_and_screen[1]]
            # print(app_cors)
            if 0 > app_cors[0]:
                app_cors[0] = 0
            elif max_coordinates[0] < app_cors[0]:
                app_cors[0] = max_coordinates[0]
            # print(app_cors)
            if 0 > app_cors[1]:
                app_cors[1] = 0
            elif max_coordinates[1] < app_cors[1]:
                app_cors[1] = max_coordinates[1]
            app.geometry(f"350x350+{app_cors[0]}+{app_cors[1]}")
            
    last_click = 0
    def check_click(x, y, button, pressed):
        global move_click, definition_mouse_and_screen
        # Проверяем, находится ли курсор на слайдере перемещения в момент нажатия
        if pressed:
            global last_click
            if str(button) == "Button.left":
                if (app.winfo_x() + blank_space < x < app.winfo_x() + blank_space + background.winfo_width() and
                    app.winfo_y() + app.winfo_height() - background.winfo_height() < y < app.winfo_y() + app.winfo_height()):
                    if 0 < time.time() - last_click < 0.7:
                        if main_app.main_app_existing != True:

                            main_app.activate_window(data, data_reg_window_fun, database_functions)
                    else:
                        definition_mouse_and_screen = (app.winfo_x() - x, app.winfo_y() - y)
                        move_click = True
                    last_click = time.time()
        else:
            if move_click and str(button) == "Button.left":
                move_click = False
                # Потом поместить сюда функцию для запоминая
                # координат виджета у json файл

    move_listener = pynput.mouse.Listener(check_move, check_click)


    def open_app():
        app.deiconify()
        app.lower()
        app.after(5000, open_app)
        
    def update_temp_label():
        global weather_id
        api_data = api.get_api_data(city)
        
        # api_data = {"a": 1}
        
        # try:
        temp = round(api_data["current"]["temp_c"])
        if -15 < temp < 35:
            bg_color = ("#4dbbff", "#2457ff", "#7c849c", "#facc61", "#ffa02b", "#994000")
            bg_color = bg_color[round((temp / 7 + 2) // 1)]
        elif -15 >= temp:
            bg_color = "#c7f2fc"
        elif temp >= 35: 
            bg_color = "#ff2a00"
        weather_all = translator.translate(api_data['current']['condition']['text']).split(" ")
        weather = weather_all[0]
        del weather_all[0]
        weather_full = " ".join(weather_all)
        icon_image = f"http:{api_data['current']['condition']['icon']}"
        tempa = api_data['forecast']['forecastday'][0]['day']
        min_max_temperature_text = f"🠕{round(tempa['maxtemp_c'])}° 🠗{round(tempa['mintemp_c'])}°"
        
        # except:
        #     temp = "ℵ1"
        #     bg_color = "#c300ff"
        #     # city = "Milky Way"
        #     icon_image = "https://www.worldit.academy/media/staff/photo/IMG_0016.jpeg"
        #     weather = "Nuclear winter"
        #     min_max_temperature_text = "🠕SSGG(3)° 🠗-TREE(3)°"
        
        reset_button.configure(True, hover_color = bg_color)
        background.configure(True, fg_color = bg_color)
        temp_label.configure(True, text = f"{temp}º")
        city_label.configure(True, text = city)
        weather_text.configure(True, text = weather)
        weather_full_text.configure(True, text = weather_full)
        min_max_temperature.configure(True, text = min_max_temperature_text)
        
        os.chdir(f_path.search_path("images\\icons"))
        icon_name = api_data['current']['condition']['text'].split(" ")
        icon_name = f"{api_data['current']['condition']['text']}_icon.png"
        urllib.request.urlretrieve(icon_image, icon_name)
        weather_icon.configure(True, image = ctk.CTkImage(Image.open(icon_name), size = (180, 142)))
        os.chdir(__file__ + "/..")

        if weather_id != None:
            app.after_cancel(weather_id)
        weather_id = app.after(600000, update_temp_label)
    

    reset_button.configure(False, command = update_temp_label)


    app.overrideredirect(1)
        
    update_temp_label()
    open_app()
    move_listener.start()


    background.place(x = 0, y = 0)
    temp_label.place(x = 340, y = 200, anchor = "e")
    city_label.place(x = 340, y = 300, anchor = "e")
    weather_icon.place(x = 18, y = 17)
    weather_text.place(x = 18, y = 162)
    weather_full_text.place(x = 18, y = 198)
    min_max_temperature.place(x = 18, y = 228)
    reset_button.place(x = 343, y = 18, anchor = "ne")
    app.mainloop()