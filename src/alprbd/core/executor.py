# -*- coding: utf-8 -*-
"""Unlicensed"""

def Execute(node):
    """Process a Node and produce result"""
    if not callable(node.data):
        return node.data
    # end if
    return None
# end def
