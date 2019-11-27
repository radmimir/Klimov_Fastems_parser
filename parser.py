import os

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
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
    in_dir = os.path.join(dirname, 'files\\')
    out_dir = os.path.join(dirname, 'result\\')
    out_dir = os.path.join(dirname, 'result\\')
    x_ar, y_ar, z_ar = [], [], []
    if os.path.exists(in_dir):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        n = len(os.listdir(in_dir))
        k = 0
        if n != 0:
            for file in os.listdir(in_dir):
                x_ar, y_ar, z_ar = np.array([]), np.array([]), np.array([])
                x_ard, y_ard, z_ard = np.array([]), np.array([]), np.array([])
                infile_name = in_dir + file
                outfile_name_up = out_dir + file[:-8] + "_up.txt"  # out_dir +
                outfile_name_down = out_dir + file[:-8] + "_down.txt"  # out_dir +
                print(k + 1, "Запись. Имя файла=", infile_name)
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
                        y_up = list(map(lambda t: t / DOTS_OFFSET, a[2:data_cnt + 2]))
                        # filter(lambda t: t != Y_ZERO, a[2:data_cnt + 2]))
                        y_down = list(map(lambda t: t / DOTS_OFFSET, a[data_cnt + 2:2 * data_cnt + 2]))
                        # filter(lambda t: t != Y_ZERO, a[data_cnt + 2:2 * data_cnt + 2]))
                        z = round(a[1] / 10 ** 3 - 7000, 2)  # Позиция Энкодера
                        for y in y_up:
                            if y != Y_ZERO / DOTS_OFFSET:
                                outstr_up = "{0};{1};{2}\n".format(x, y, z)  # форматирование строки
                                """if z == 717.3919:
                                    x_ar = np.append(x_ar, x)
                                    y_ar = np.append(y_ar, y)
                                    z_ar = np.append(z_ar, z)"""
                                x_ar = np.append(x_ar, x)
                                y_ar = np.append(y_ar, y)
                                z_ar = np.append(z_ar, z)
                                outfile_up.write(outstr_up)
                                x = round(x + xpitch, 2)
                            else:
                                x = round(x + xpitch, 2)
                                continue
                        x = xstart
                        for y in y_down:
                            if y != Y_ZERO / DOTS_OFFSET:
                                outstr_down = "{0};{1};{2}\n".format(-x, -y, z)  # форматирование строки
                                outfile_down.write(outstr_down)
                                x_ard = np.append(x_ard, x)  # x + 1.5)
                                y_ard = np.append(y_ard, y)  # -y + 19)
                                z_ard = np.append(z_ard, z)
                                x = round(x + xpitch, 2)
                            else:
                                x = round(x + xpitch, 2)
                                continue
                    break
                except IndexError:
                    print(j)
                outfile_up.close()
                outfile_down.close()
            print("Всего", 2 * k, "файлов записано.")
        else:
            print("Папка с данными files пуста.")
    else:
        print("Папка с данными files не существует. Поместите исполняемый файл в папку files.")
    # print(x_ar)
    # print(y_ar)
    # print(z_ar)
    # fig = go.Figure(data=[go.Surface(x=x_ar, y=y_ar, z=z_ar)])
    # fig.show()
    x_ar, y_ar, z_ar = np_optim(x_ar, y_ar, z_ar)
    graph3d(x_ar, y_ar, z_ar, x_ard, y_ard, z_ard)
    return 0


def np_optim(x, y, z):
    xyz = np.array((x, y, z), dtype='float')
    xyz = xyz[xyz[:, 2].argsort()]
    x1, y1, z1 = xyz
    n = len(x1)
    x2, y2, z2 = [], [], []
    for i in range(0, n, 5):
        x2.append(x1[i])
        y2.append(y1[i])
        z2.append(z1[i])
    return x2, y2, z2


def graph3d(x1, y1, z1, x2, y2, z2):  # , q):
    fig = plt.figure()
    ax = Axes3D(fig)
    """xyz1 = np.array((x1, y1, z1), dtype='float')
    xyz2 = np.array((x2, y2, z2), dtype='float')
    xyz1 = xyz1[xyz1[:, 0].argsort()]
    x1, y1, z1 = xyz1
    xyz2 = xyz2[xyz2[:, 0].argsort()]
    x2, y2, z2 = xyz2"""
    for z in z1:
        ax.plot3D(x1, y1, z)
    for z in z2:
        ax.plot3D(x2, y2, z)
    # ax.plot_trisurf(x1, y1, z1)
    # ax.plot_trisurf(x2, y2, z2, color='red')
    ax.view_init(50, -45)
    if not os.path.exists('frames'):
        os.mkdir('frames')
    else:
        for file in os.listdir('frames'):
            os.unlink(os.path.join('frames/', file))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # Мы собираемся сделать 20 графиков, для 20 разных углов
    """for angle in range(70, 270, 2):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(x1, y1, z1, linewidth=0.2)
        ax.plot_trisurf(x2, y2, z2, linewidth=0.2, color='red')

        ax.view_init(angle - 70, angle)

        filename = 'frames/step' + str(angle) + '.png'
        plt.savefig(filename, dpi=96)
        plt.gca()
        plt.close(fig)"""
    # ax.scatter(x1, x2, yy)  # построение графика аппроксимации
    # ax.scatter(x1, x2, q)  # построение графика исходных
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    os.system('convert -delay 10 step*.png animated_3d.gif')
    plt.show()


if __name__ == '__main__':
    main()
