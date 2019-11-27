import os

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Константы
PARAMS_OFFSET = 10 ** 5  # Смещение параметров
FILE_OFFSET = 6  # Смещение начала данных
DOTS_OFFSET = 10 ** 5  # смещение точек
Y_ZERO = -2147483648  # Смещение y
th = ["X_UP", "Y_UP", "Z_UP", " ", "X_DOWN", "Y_DOWN", "Z_DOWN"]  # Подписи столбцов


def main():
    dirname = os.path.dirname(__file__)
    in_dir = os.path.join(dirname, 'result\\')
    x_ar, y_ar, z_ar = [], [], []
    k = 0
    for file in os.listdir(in_dir):
        x_ar, y_ar, z_ar = np.array([]), np.array([]), np.array([])
        x_ard, y_ard, z_ard = np.array([]), np.array([]), np.array([])
        infile_name = in_dir + file
        print(k + 1, "Чтение. Имя файла=", infile_name)
        k += 1
        with open(infile_name, 'r') as f:
            inp = f.readlines()  # Входные данные
        # Запишем параметры считывания
        params = list(map(int, inp[4].split(';')))
        xpitch = params[2] / PARAMS_OFFSET  # шаг
        xstart = params[3] / PARAMS_OFFSET  # Начальное значение x
        data_cnt = params[4]  # Количество точек на срезе
        xstop = xstart + xpitch * data_cnt  # Конечный x
        n = len(inp)  # Количество строк в файле
        # Инициализация переменных
        out = []  # Выходной массив
        # Цикл по строкам
        outfile_up = open(outfile_name_up, 'w')
        outfile_down = open(outfile_name_down, 'w')
        try:
            for i in range(FILE_OFFSET, n, 1):
                x = xstart
                a = list(map(int, inp[i].split(';')[:-1]))
                y_up = map(lambda t: t / DOTS_OFFSET, a[2:data_cnt + 2])
                # filter(lambda t: t != Y_ZERO, a[2:data_cnt + 2]))
                y_down = map(lambda t: t / DOTS_OFFSET, a[data_cnt + 2:2 * data_cnt + 2])
                # filter(lambda t: t != Y_ZERO, a[data_cnt + 2:2 * data_cnt + 2]))
                z = round(a[1] / 10 ** 3 - 7000, 2)  # Позиция Энкодера
                for y in y_up:
                    if y != Y_ZERO / DOTS_OFFSET:
                        outstr_up = "{0};{1};{2}\n".format(x, y, z)  # форматирование строки
                        """if z == 717.3919:
                            x_ar = np.append(x_ar, x)
                            y_ar = np.append(y_ar, y)
                            z_ar = np.append(z_ar, z)"""
                        """x_ar = np.append(x_ar, x)
                        y_ar = np.append(y_ar, y)
                        z_ar = np.append(z_ar, z)"""
                        outfile_up.write(outstr_up)
                        x = round(x + xpitch, 2)
                    else:
                        x = round(x + xpitch, 2)
                        continue
                for y in y_down:
                    if y != Y_ZERO / DOTS_OFFSET:
                        outstr_down = "{0};{1};{2}\n".format(x, y, z)  # форматирование строки
                        outfile_down.write(outstr_down)
                        """x_ard = np.append(x_ard, x)
                        y_ard = np.append(y_ard, y)
                        z_ard = np.append(z_ard, z)"""
                        x = round(x + xpitch, 2)
                    else:
                        x = round(x + xpitch, 2)
                        continue
        except IndexError:
            print(j)
        outfile_up.close()
        outfile_down.close()
    print("Всего", 2 * k, "файлов записано.")
    # print(x_ar)
    # print(y_ar)
    # print(z_ar)
    # fig = go.Figure(data=[go.Surface(x=x_ar, y=y_ar, z=z_ar)])
    # fig.show()
    # graph3d(list(x_ard), list(y_ard), list(z_ard))
    return 0


"""def graph3d(x1, x2, yy):  # , q):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_trisurf(x1, x2, yy, color='orange')
    # ax.scatter(x1, x2, yy)  # построение графика аппроксимации
    # ax.scatter(x1, x2, q)  # построение графика исходных
    xs = np.zeros(1000)
    ys = np.zeros(1000)
    zs = np.array([i for i in range(42700, 43700)])
    # ax.plot3D(xs, ys, zs)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()"""


if __name__ == '__main__':
    main()
