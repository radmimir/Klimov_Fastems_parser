from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from constants import constants


def graph3d(x, y, z):  # построение модели
    fig = plt.figure()
    ax = Axes3D(fig)
    n = len(x)
    const = constants()
    print("Graph 3D plotting", n, "graphs...")
    for i in range(len(x)):
        ax.scatter(x[i], y[i], z[i], s=1., c=const['colors'][i])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend(['Up', 'Down'])
    ax.view_init(90, 180)
    plt.show()
