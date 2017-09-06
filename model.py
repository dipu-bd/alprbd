""" Unlicensed """
from node import Node, Var
from skimage.io import imread
from skimage.transform import resize

IMAGE = 'jpg'
ARRAY = 'txt'

def Model():
    """Get an operational model"""
    m = dict()
    m['_file'] = Var(None)
    m['open'] = Node(imread, m['_file'], ext=IMAGE)
    m['resize'] = Node(resize, m['open'], Var(480, 640), mode='wrap', ext=IMAGE)


    return m
# end def
