import numpy as np

dist_threshold = 50
size_threshold = 10

last_frame_squares = []


def average_squares(squares):
    new_squares = []
    for (x, y, w, h) in squares:
        for (_x, _y, _w, _h) in last_frame_squares:
            dist_x = np.positive(x - _x)
            dist_y = np.positive(y - _y)
            size_w = np.positive(w - _w)
            size_h = np.positive(h - _h)
            if dist_x < dist_threshold and dist_y < dist_threshold and \
                    size_w < size_threshold and size_h < dist_threshold:
                new_squares.append([int(_sum / 2) for _sum in [(x + _x), (y + _y), (w + _w), (h + _h)]])
                break

    last_frame_squares.clear()
    last_frame_squares.extend(squares)

    return np.array(new_squares)
