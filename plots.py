import numpy as np
from os import path

import plotly.offline as py
import plotly.graph_objs as go

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
    save_kernel("Gaussian Kernel", gauss)

    print("Saving matched filter...")
    mixture = MatchFilter.mixture_model()
    save_kernel("Mixture Model", mixture)

    print("Saving weight function...")
    save_weight_function("Weight Distribution")

    print("Saved all plots!\n")
# end function


def save_kernel(title, kernel):
    py.init_notebook_mode()
    data = [
        go.Surface(
            z=kernel
        )
    ]
    layout = go.Layout(
        title=title,
    )
    fig = go.Figure(data=data, layout=layout)

    py.iplot(fig)
# end function


def save_weight_function(title):
    wfunc = np.vectorize(Intensify.weight)
    x = np.arange(0, 1, 0.001, dtype=np.float64)
    y = wfunc(x)


# end function


if __name__ == '__main__':
    save_all()
# end if
