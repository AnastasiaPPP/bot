import pathlib
def new_entry(text):
    path = pathlib.Path.cwd()
    with open(f'{path}' + '\data_file.txt', 'a', encoding='utf-8') as data:
        data.write(f'{text}\n')



def show_data():
    path = f'{pathlib.Path.cwd()}' + '\data_file.txt' 
    with open(path, 'r', encoding='utf-8') as data:
        names = []
        lines = data.readlines()
        for line in lines:
            names.append(line)
    return names


