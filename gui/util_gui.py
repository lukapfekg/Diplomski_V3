def calculate_size(c_width, c_height, i_width, i_height):
    if i_width <= i_height:
        odnos = c_height / i_height
    else:
        odnos = c_width / i_width

    w = round(odnos * i_width)
    h = round(odnos * i_height)

    return w, h