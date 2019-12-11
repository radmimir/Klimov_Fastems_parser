#import math
from constants import constants
# import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from numpy import append, bitwise_and, where

MAXDOUBLE = 2147483648.
MINDOUBLE = -2147483648.


def rect(r, phi):
    x = r * math.cos(phi)
    y = r * math.sin(phi)
    return x, y


def polar(x, y):
    r = (x ** 2 + y ** 2) ** .5
    phi = math.atan2(y, x)
    return r, phi


def rotate_polar(x, y, offset_phi):
    r, phi = polar(x, y)
    phi += offset_phi
    x, y = rect(r, phi)
    return x, y


def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def np_optim(x, y, z, offset):  # xyz numpy arrays optimization, z - must be sorted
    xyz = array((x, y, z), dtype='float')
    xyz = xyz[xyz[:, 1].argsort()]
    # print(xyz)
    x1, y1, z1 = xyz
    n = len(x1)
    x2, y2, z2 = [], [], []
    # a = list(z1).index(offset)
    x1, y1, z1 = xyz
    for i in range(0, n, 5):
        x2.append(x1[i])
        y2.append(y1[i])
        z2.append(z1[i])
    return x2, y2, z2


def make_gif(x, y, z):
    n = len(x)
    if not os.path.exists('frames'):  # проверка наличия пути сохранения
        os.mkdir('frames')
    else:
        for file in os.listdir('frames'):
            os.unlink(os.path.join('frames/', file))
    # Мы собираемся сделать 20 графиков, для 20 разных углов
    for angle in range(70, 270, 2):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for i in range(n):
            ax.scatter(x[i], y[i], z[i], s=1.)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.view_init(30, angle)

        filename = 'frames/step' + str(angle) + '.png'
        plt.savefig(filename, dpi=96)
        plt.gca()
        plt.close(fig)


def graph3d(x, y, z):  # построение модели и выгрузка в gif - файл
    fig = plt.figure()
    ax = Axes3D(fig)
    dict_z1 = {}
    n = len(x)
    const = constants()
    print("Graph 3D plotting", n, "graphs...")
    for i in range(len(x)):
        ax.scatter(x[i], y[i], z[i], s=1., c=const['colors'][i])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend(['Up', 'Down'])
    ax.view_init(90, -200)
    plt.show()


def offset(x, y, z, consts, offset_x=0, offset_y=0, offset_z=0):
    if offset_x or offset_y or offset_z:
        x += offset_x
        y += offset_y
        z += offset_z
    else:
        x += consts['offset_x']
        y += consts['offset_y']
        z += consts['offset_z']
    return x, y, z


def convert3d_arrays_to_list_of_tuples(data, dec):  # list of 3d numpy arrays
    x, y, z = [], [], []
    for arr in data:
        x = x.extend(arr[:, 0][::dec])
        y = y.extend(arr[:, 1][::dec])
        z = z.extend(arr[:, 2][::dec])


def filter3d(data, filter):  # takes 3d numpy array [[x0,y0,z0],[x1,y1,z1]...]
    # minx,maxx,miny,maxy,minz,maxz
    cond1 = bitwise_and(data[:, 0] > filter[0], data[:, 0] < filter[1])
    cond2 = bitwise_and(data[:, 1] > filter[2], data[:, 1] < filter[3])
    cond3 = bitwise_and(data[:, 2] > filter[4], data[:, 2] < filter[5])
    cond = bitwise_and(cond1, cond2)
    cond = bitwise_and(cond, cond3)
    data = data[where(cond)]
    """x, y, z = array(data[:, 0]), array(data[:, 1]), array(data[:, 2])
    x = x[where(bitwise_and(data[:, 0] > filter[0], data[:, 0] < filter[1]))]
    y = y[where(bitwise_and(data[:, 1] > filter[2], data[:, 1] < filter[3]))]
    z = z[where(bitwise_and(data[:, 2] > filter[4], data[:, 2] < filter[5]))]"""
    """data = array()
    data = append(data, x)
    data = append(data, y)
    data = append(data, z)
    print(data)
    x, y, z = x[0:, ], y[0:, ], z[0:, ]"""
    """for i in range(n):
        m = len(x[i])
        for j in range(m):
            x1 = x[i][j]
            y1 = y[i][j]
            z1 = z[i][j]
            if x1 < filter[0] or x1 > filter[1] or y1 < filter[2] or y1 > filter[3] or z1 < filter[4] or z1 > filter[5]:
                delete()"""
    return data
