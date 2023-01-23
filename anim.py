import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as anim

# N = [3, 5]
N = [5]
M = 64
x = np.linspace(0, 2 * np.pi, 6000)


def showChart(n: int):
    plt.axes(projection='polar')
    plt.polar(x, np.sin(n * x + (np.pi / 10)))
    # plt.show()


def main():
    for n in N:
        showChart(n)


for n in N:
    lines = 8
    frames = 256//lines
    # m = np.linspace((-M/2), M/2, M*4)
    m = np.linspace((-M / 2), M / 2, frames*2)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    line, = ax.plot([], [], 'r')
    plt.axis('off')

    def updateChart(b: int):
        r = np.sin(n * x + (b*np.pi / 10))
        line.set_data(x, r)
        return line,


    an = anim.FuncAnimation(fig, updateChart, frames=m, interval=lines/100, repeat=True, blit=True)
    an.save('aliasing/animation.gif', writer='imagemagick', fps=60)
    plt.show()


if __name__ == '__main__':
    main()