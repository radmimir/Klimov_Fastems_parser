import os
import cmath, math

from mpl_toolkits.mplot3d import Axes3D
from itertools import groupby
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import locale
import gc
from constants import constants as cnt
import convert, tools
from scipy import ndimage
import statistics as sts
import sys
from collections import Mapping, Container
from sys import getsizeof


def main():
    (x_up, x_down), (y_up, y_down), (z_up, z_down) = convert.convert(1)
    os.system('chcp 668>nul')
    constants = cnt()
    Wing_offset_up = 0.01  # 153.02
    Wing_offset_down = 0.01  # 154.22
    # x_up, y_up, z_up = tools.np_optim(x_up, y_up, z_up, Wing_offset_up)
    # x_down, y_down, z_down = tools.np_optim(x_down, y_down, z_down, Wing_offset_down)
    # Попытка отсортировать по словарю - вылет по памяти
    """d_up = dict.fromkeys(z_up, [])
    d_down = dict.fromkeys(z_down, [])
    for j in range(len(z_up)):
        d_up[z_up[j]].append([x_up[j], y_up[j]])
    for j in range(len(z_down)):
        d_down[z_down[j]].append([x_down[j], y_down[j]])
    sorted_keys_up = sorted(z_up)
    sorted_keys_down = sorted(z_down)
    print(deep_getsizeof(d_up), sys.getsizeof(sorted_keys_up))
    x_up, y_up, z_up, x_down, y_down, z_down = [], [], [], [], [], []
    for key in sorted_keys_up:
        for dot_xy in d_up[key]:
            x_up.append(dot_xy[0])
            y_up.append(dot_xy[1])
            z_up.append(key)
    for key in sorted_keys_down:
        for dot_xy in d_down[key]:
            x_down.append(dot_xy[0])
            y_down.append(dot_xy[1])
            z_down.append(key)"""

    x, y, z = ([x_up[::5], x_down[::5]], [y_up[::5], y_down[::5]],
               [z_up[::5], z_down[::5]])
    (x_up, x_down), (y_up, y_down), (z_up, z_down) = x, y, z
    n = len(z_up)
    # tools.graph3d(x, y, z)
    x_up, y_up, z_up = tools.offset(x_up, y_up, z_up, constants)
    x_down, y_down, z_down = tools.offset(x_down, y_down, z_down, constants)
    for j in range(n):
        x_up[j], z_up[j] = tools.rotate_polar(x_up[j], z_up[j], offset_phi=constants['y_rotate'])
        x_up[j], y_up[j] = tools.rotate_polar(x_up[j], y_up[j], offset_phi=constants['z_rotate'])
        y_up[j], z_up[j] = tools.rotate_polar(y_up[j], z_up[j], offset_phi=constants['x_rotate'])
    x_down, y_down, z_down = tools.offset(x_down, y_down, z_down, constants, offset_x=-5, offset_y=-2.75)
    x1, y1, z1 = (x_up, x_down), (y_up, y_down), (z_up, z_down)
    # удаление "плохих" точек
    """for i in range(len(x)):
        for j in range(len(z[i])):
            try:
                if j >= len(z[i]):
                    break
                if z[i][j] < 0 or y[i][j] > 15:
                    print("deleted: ", i, j, x[i][j], y[i][j], z[i][j])
                    x[i][j] = np.delete(x[i], j, 0)
                    y[i][j] = np.delete(y[i], j, 0)
                    z[i][j] = np.delete(z[i], j, 0)
            except IndexError:
                print(i, j, len(x[i]), len(y[i]), len(z[i]))"""
    # x[i] = list(ndimage.gaussian_filter(x[i], sigma=sts.stdev(x[i])))
    # y[i] = list(ndimage.gaussian_filter(y[i], sigma=sts.stdev(y[i])))
    # z[i] = list(ndimage.gaussian_filter(z[i], sigma=sts.stdev(z[i])))
    tools.graph3d(x1, y1, z1)
    return 0


if __name__ == '__main__':
    main()
