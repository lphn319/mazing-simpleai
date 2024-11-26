def load_map(map_str):
    return [list(row) for row in map_str.split("\n") if row]

def is_valid_point(map_data, x, y):
    return map_data[y][x] != '#'

def is_valid_path(x1, y1, x2, y2):
    return (x1,y1) != (x2,y2)