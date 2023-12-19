from json import load, dump
    
def json_creater(data, path: str):
    with open(f'{path}', 'w+', encoding = 'UTF-8') as file:
        dump(data, file, indent = 4)  

def json_load(path: str):
    with open(f'{path}', 'r', encoding = 'UTF-8') as file:
        return load(file)