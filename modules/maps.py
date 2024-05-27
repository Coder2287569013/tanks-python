import os

maps_folder = os.path.join(os.path.dirname(__file__), "../maps")
content = os.listdir(maps_folder) 
map_data = [os.path.join(maps_folder, file) 
            for file in content if file.endswith(".txt")]

def load_map(map_data, index, char):
    with open(map_data[index], "r") as file:
        data = file.read()
        return [[char[obj] for obj in row] for row in data.splitlines()]
                