
def color_converter(color):
    if color == "black":
        return [0, 0, 0]
    if color == "lightgrey":
        return [0.7, 0.7, 0.7]
    if color == "grey":
        return [0.5, 0.5, 0.5]
    if color == "red":
        return [1.0, 0.1, 0.1]
    if color == "blue":
        return [0.1, 0.1, 1.0]
    if color == "green":
        return [0.1, 1.0, 0.1]
    return color

