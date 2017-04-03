from os import path

from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from helper import *
from modules import Gaussian
from modules import MatchFilter
from modules import Intensify


def save_all():
    """
    save all plots to output directory 
    """
    out = util.output_path()

    print("Saving gaussian kernel...")
    gauss = Gaussian.blur_kernel()
    save_kernel(path.join(out, "gaussian.png"), gauss)

    print("Saving matched filter...")
    mixture = MatchFilter.mixture_model()
    save_kernel(path.join(out, "mixture.png"), mixture)

    print("Saving weight function...")
    save_weight_function(path.join(out, "weight.png"))

    print("Saved all plots!\n")
# end function


def save_plot(X, Y, Z, fileName):
    """    
    :param X: 
    :param Y: 
    :param Z: 
    :param fileName: 
    :return: 
    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.view_init(20, 45)

    surf = ax.plot_surface(X, Y, Z,
                           rstride=1,
                           cstride=1,
                           color='w',
                           linewidth=0.02)
                           #cmap = cm.coolwarm,
                           #antialiased=False)

    #fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('Width')
    ax.set_ylabel('Height')
    ax.set_zlabel('Value')

    plt.savefig(fileName)
    plt.clf()
    plt.close()
# end function


def save_kernel(fileName, kernel):
    """    
    :param fileName: 
    :param kernel: 
    :return: 
    """
    m, n = cfg.BLUR_SIZE

    X = np.arange(m)
    Y = np.arange(n)
    X, Y = np.meshgrid(X, Y)
    Z = kernel

    save_plot(X, Y, Z, fileName)
# end function


def save_weight_function(fileName):
    """    
    :param fileName: 
    :return: 
    """
    wfunc = np.vectorize(tools.weight)
    x = np.arange(0, 1, 0.001, dtype=np.float64)
    y = wfunc(x)

    plt.plot(x, y)
    plt.xlim(0, 1)
    plt.ylim(0, 3)

    plt.savefig(fileName)
    plt.clf()
    plt.close()
# end function


if __name__ == '__main__':
    saveAll()
# end if
