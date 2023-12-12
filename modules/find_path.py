import os
def search_path(file_name: str):
    abs_path = os.path.abspath(__file__ + "/.." + "/..")
    abs_path = os.path.join(abs_path, file_name)
    return abs_path
