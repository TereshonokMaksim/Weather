import customtkinter as ctk
import json, os, time
from deep_translator.google import GoogleTranslator
import modules.widget as widget
import modules.database as database
import modules.find_path as fp

dict_entry_field, ID, user_data, count_app = None, None, None, 0


def launch_widget(window = None):
    global widget_launched
    if window != None:
        window.destroy()
    if widget.widget_launched is not 1:
        widget_launched = 1
        widget.create_widget(database.read_data_by_id(), create_data_reg_window, {"add": database.add_data, "read": database.read_data_by_id, "edit": database.edit_data})

def create_data_reg_window():
    global dict_entry_field, ID, user_data, count_app
    count_app += 1
    print("start reg_window")
    translate = GoogleTranslator()
    app_size = (465, 645)
    reg_app = ctk.CTkToplevel()
    reg_app.geometry(f"{app_size[0]}x{app_size[1]}+{(reg_app.winfo_screenwidth() - app_size[0]) // 2}+{(reg_app.winfo_screenheight() - app_size[1]) // 2}")
    reg_app.title(f"Error! Code RA{count_app}")

    open_widget = lambda: launch_widget(reg_app)

    UNDERLINE_FONT = ctk.CTkFont("Roboto Slab", size = 28, weight = "bold", underline = True)
    STANDART_FONT = ctk.CTkFont("Roboto Slab", size = 22)
    user_data = {
        "Країна": "Десь у космосі",
        "Місто": "Десь у Молочному шляху",
        "Ім'я": "Розумний",
        "Прізвище": "Велетень"
    }

    TRANSPARENT = reg_app._apply_appearance_mode(['#f2f2f2','#000001'])
    reg_app.attributes("-transparentcolor", TRANSPARENT)
    reg_app.config(background = TRANSPARENT)

    window = ctk.CTkFrame(
        master = reg_app, width = 460, height = 645, 
        corner_radius = 20, border_width = 5, fg_color = "#5da7b1", 
        border_color = "#096c82", bg_color = TRANSPARENT,
        background_corner_colors = (None, None, None, None)
    )

    main_text = ctk.CTkLabel(
        master = window, width = 0, height = 55, 
        font = ctk.CTkFont("Roboto Slab", 28), text = "Реєстрація користувача",
        text_color = "#ffffff", fg_color = "transparent"
        )

    button_save = ctk.CTkButton(
        master = window, width = 218, height = 46,
        corner_radius = 20, border_width = 3,
        fg_color = "#096c82", border_color = "#dbdbdb",
        text = "Зберегти", font = STANDART_FONT,
        text_color = "#dbdbdb", command = lambda: 1 + 1,
        hover_color = "#4a878f"
        )

    reg_app.overrideredirect(1)

    def add_entry_field(name: str, width: int = 0, coors: tuple = ("x", "y"), mode: str = "TEXT/ENTRY"):
        # Если mode это ENTRY тогда создает поля ввода для каждого заголовка
        # если же mode это TEXT тогда создает вместо полей ввода текст с информацией которую вводили до этого
        global dict_entry_field
        text = ctk.CTkLabel(
                            master = window, width = 0, height = 31, 
                            text = name, font = STANDART_FONT,
                            fg_color = "transparent", text_color = "#ffffff"
                            )
        if mode == "ENTRY":
            output = ctk.CTkEntry(
                                    master = window, width = width, height = 46,
                                    corner_radius = 20, border_width = 3,
                                    fg_color = "#096c82", border_color = "#dbdbdb"
                                    )
            x_offset = 42
        elif mode == "TEXT":
            output = ctk.CTkLabel(
                master = window, width = 0, height = 55, 
                font = UNDERLINE_FONT, text = user_data[name],
                text_color = "#ffffff", fg_color = "transparent"
                )
            x_offset = 86
        text.place(x = coors[0] + 8, y = coors[1])
        output.place(x = coors[0] + x_offset, y = coors[1] + 39)
        return {name: output}

    dict_entry_field = {}
    # Как построен словарь:
    # Название поля ввода: ширина поля ввода
    dict_name = {"Країна": 218, "Місто": 218, "Ім'я": 295, "Прізвище": 295}
    y = 108
    mode = "ENTRY"
    button_data = []
    change_button = False

    for name in dict_name:
        print(dict_entry_field)
        dict_entry_field.update(add_entry_field(name, dict_name[name], (38, y), mode))
        y = y + 99

    def save_data():
        country = dict_entry_field["Країна"].get()
        city = dict_entry_field["Місто"].get()
        name = dict_entry_field["Ім'я"].get()
        surname = dict_entry_field["Прізвище"].get()
        print(country, city, name, surname)
        if "" not in (country, city, name, surname) and " " not in (country, city, name, surname):
            time.sleep(1.5)
            if not os.path.exists(fp.search_path("data\\id.json")):
                with open(fp.search_path('data\\id.json'), "w") as file:
                    ID = len(database.read_data("main_data")) - 1
                    json.dump({"ID": ID}, file)
            else:
                with open(fp.search_path('data\\id.json'), "r") as file:
                    ID = json.load(file)["ID"]
            database.add_data("main_data", {
                "ID": ID,
                "Country": country,
                "City": city,
                "Name": name,
                "Surname": surname
            })
            show_data()
        else:
            main_text.configure(True, text = "Одно або декілька полів порожні")


    def show_data():
        global dict_entry_field, ID, user_data
        with open(fp.search_path('data\\id.json'), "r") as file:
            ID = json.load(file)["ID"]
        data = database.read_data("main_data")
        # try:
        data = database.read_data("main_data")[ID + 1]
        # except:
        #     print("database read error")
        #     data = [0, "Десь у космосі", "Десь у Молочному шляху", "Розумний", "Велетень"]
        user_data = {
            "Країна": data[1],
            "Місто": data[2],
            "Ім'я": data[3],
            "Прізвище": data[4]
        }
        y = 108
        print(dict_entry_field)
        for count in range(len(dict_entry_field)):
            dict_entry_field[list(dict_entry_field)[count]].destroy()
            
        for name in user_data:
            dict_entry_field.update(add_entry_field(name, 0, (38, y), "TEXT"))
            y += 99
        button_save.configure(True, text = "Перейти до додатку", command = open_widget)

    if change_button:
        button_save.configure(True, command = open_widget, text = "Перейти до додатку")
    else:
        button_save.configure(False, command = save_data)
    with open(fp.search_path("data\\id.json")) as file:
        ID = json.load(file)["ID"]
    if len(database.read_data_by_id()) >= ID - 2:
        show_data()
    window.place(x = 0, y = 0)
    main_text.place(x = app_size[0] // 2, y = 42, anchor = "n")
    button_save.place(x = app_size[0] // 2, y = 546, anchor = "n")
    print("end reg window")
    reg_app.mainloop()



if os.path.exists(fp.search_path("data\\id.json")):
    with open(fp.search_path("data\\id.json"), "r") as file:
        ID = json.load(file)["ID"]
    data = database.read_data_by_id()
    print(data)
    if type(data) == dict:
        print("data")
        
        launch_widget()
    else:
        create_data_reg_window()
else:
    create_data_reg_window()
