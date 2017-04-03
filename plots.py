import cv2
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
    save_kernel(Gaussian.blur_kernel())

    print("Saving matched filter...")
    save_kernel(MatchFilter.mixture_model())

    print("Saving weight function...")
    save_weight_function()

    print("Saving segments function...") 
    save_segment_graph(path.join("stages","stage.16","01.00.wnb.jpg"))

    print("Saved all plots!\n")
# end function


def save_kernel(kernel):
    data = [
        go.Surface(
            z = kernel
        )
    ]
    layout = go.Layout(
        xaxis = dict(title = 'width'),
        yaxis = dict(title = 'height')
    )
    fig = go.Figure(
        data=data, 
        layout=layout
    )

    py.init_notebook_mode()
    py.iplot(fig)
# end function


def save_weight_function():
    wfunc = np.vectorize(Intensify.weight)
    random_x = np.linspace(0, 1, 1000)
    random_y = wfunc(random_x)

    # Create a trace
    data = [
        go.Scatter(
            x = random_x,
            y = random_y
        )
    ]
    layout = go.Layout(
        xaxis = dict(title = 'Normalized Edge Density'),
        yaxis = dict(title = 'Enhancement Coefficient')
    )
    fig = go.Figure(
        data=data, 
        layout=layout
    )

    py.init_notebook_mode()
    py.iplot(fig)
# end function


def save_segment_graph(file):    
    img = cv2.imread(file, cv2.CV_8UC1)
    height, width = img.shape
    
    # horizontal 
    r_x = np.linspace(0, height, height)
    r_y = np.mean(img, axis=1)
    r_l = np.mean(r_y) / 2
    row = [
        go.Scatter(
            x = r_x, 
            y = r_y
        ),
        go.Scatter(
            x = [0, height],
            y = [r_l, r_l]
        )
    ]
    print("Horizontal plot")
    py.init_notebook_mode()
    py.iplot(row)

    # vertical
    c_x = np.linspace(0, width, width)
    c_y = np.mean(img, axis=0)    
    c_l = np.mean(r_y) / 2

    col = [
        go.Scatter(
            x=c_x, 
            y=c_y
        ),
        go.Scatter(
            x = [0, width],
            y = [c_l, c_l]
        )
    ]
    print("Vertical plot")
    py.init_notebook_mode()
    py.iplot(col)
# end function

if __name__ == '__main__':
    save_all()
# end if
