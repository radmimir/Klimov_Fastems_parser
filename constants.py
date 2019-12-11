import math


def constants() -> dict:
    res = {}
    res['PARAMS_OFFSET'] = 10 ** 5  # Смещение параметров
    res['FILE_OFFSET'] = 6  # Смещение начала данных
    res['DOTS_OFFSET'] = 10 ** 5  # смещение точек
    res['Y_ZERO'] = -2147483648  # Смещение y
    res['th'] = ["X_UP", "Y_UP", "Z_UP", " ", "X_DOWN", "Y_DOWN", "Z_DOWN"]  # Подписи столбцов
    res['offset_x'] = 3.564
    res['offset_y'] = -8.488
    res['offset_z'] = 0.326
    res['z_offset'] = 16645.0
    res['x_rotate'] = math.radians(3.5)
    res['y_rotate'] = 0
    res['z_rotate'] = math.radians(180)  # 23.757
    res['colors'] = 'black', 'red'
    res['SMALL'] = 10 ** -3
    return res
