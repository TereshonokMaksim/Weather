import sqlite3
import os, json
import modules.find_path as fp


def create_table(name: str, columns: dict = {"column_name": "column_type"}):
    os.chdir(fp.search_path("data"))
    with sqlite3.connect("UserData.dp") as database:
        cursor = database.cursor()
        column_command = ""
        for column_name in columns:
            column_command += f", {column_name} {columns[column_name].capitalize()}" 
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({column_command[2:]})")
        database.commit()


def create_columns(name_table: str, columns: dict = {"column_name": "type_column"}):
    os.chdir(fp.search_path("data"))
    with sqlite3.connect("UserData.dp") as database:
        cursor = database.cursor()
        for column_name in columns:
            cursor.execute(f"ALTER TABLE {name_table} ADD COLUMN {column_name} {columns[column_name]}")
            database.commit()

def add_data(name_table: str = "main_data", add_info: dict = {"column name": "new_value_in_this_column"}):
    os.chdir(fp.search_path("data"))
    with sqlite3.connect("UserData.dp") as database:
        cursor = database.cursor()
        column_names = ""
        values = []
        quesion_marks = ""
        for name in add_info:
            column_names += f", {name}"
            quesion_marks += ", ?"
            values.append(add_info[name])
    
        action = f"INSERT INTO {name_table} ({column_names[2:]}) VALUES ({quesion_marks[2:]})"
        print(action, "\n", values)
        cursor.execute(action, values)
        database.commit()    
    
def read_data(name_table):

    os.chdir(fp.search_path("data"))
    with sqlite3.connect("UserData.dp") as database:
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM {name_table}")
        return cursor.fetchall()

def read_data_by_id(name_table: str = "main_data", _index_data: int = None):

    os.chdir(fp.search_path("data"))
    with sqlite3.connect("UserData.dp") as database:
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM {name_table}")
        data = cursor.fetchall()
        with open(fp.search_path("data\\id.json"), "r") as file:
            id = json.load(file)["ID"]
        if len(data) - 2 >= id:
            data = data[id + 1]
            if _index_data == None:
                return {"Country": data[1],
                        "City": data[2],
                        "Name": data[3],
                        "Surname": data[4]}
            else:
                try:
                    return {"data": data[_index_data]}
                except:
                    print(f"Error: index '{_index_data}' is not in the data list.\nMore info: \nData lenght = {len(data)},\nData type = {type(data)}.")
        else:
            print(f"Error: ID {id} is not registered.")
    
def edit_data(table_name: str = "main_data", data: dict = {"column_name": "new data"}, row: int = "auto"):

    os.chdir(fp.search_path("data"))
    with sqlite3.connect("UserData.dp") as database:
        cursor = database.cursor()
        try:
            if row == "auto":
                with open(fp.search_path("data\\id.json"), "r") as file:
                    row = json.load(file)["ID"]
        except:
            print("Failed at gaining ID from .json file")
        try:
            for column_name in data:
                cursor.execute(f"UPDATE {table_name} SET {column_name} = '{data[column_name]}' WHERE ID = {row}") 
            database.commit()
            print("task completed succefuly")
        except:
            print(f"Failed at edit data.\n\nMore info:\n\nCommand: UPDATE {table_name} SET {column_name} = '{data[column_name]}' WHERE ID = {row}")
