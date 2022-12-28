import pathlib
import csv

def converting_to_csv():
    dir_path = pathlib.Path.cwd()
    path = pathlib.Path(dir_path, 'data_file.txt')
    with open(path, 'r', encoding='utf-8') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(',') for line in stripped if line)
        dir_path = pathlib.Path.cwd()
        path = pathlib.Path(dir_path, 'data_file.scv')
        with open(path, 'w', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)
