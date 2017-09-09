# -*- coding: utf-8 -*-
"""Unlicensed"""
from collections import OrderedDict

class Node:

    def __init__(self, data, name=None):
        self.name = name
        self.data = data
        self._args = []
        self._kargs = OrderedDict()
    # end def

    @property
    def args(self):
        """Gets arguments"""
        return self._args
    # end def

    @property
    def kargs(self):
        """Gets named arguments"""
        return self._kargs
    # end def

    def get(self, key):
        """Get a named argument"""
        if key in self._kargs:
            return self._kargs[key]
        else:
            return None
        # end if
    # end def

    def append(self, *vals):
        """Appends argument to this node"""
        if len(vals) == 0:
            return self
        elif len(vals) > 1:
            return self.append(tuple(vals))
        # end if
        name = self.name + len(self._args)
        self._args.append(Node(vals[0], name=name))
        return self
    # end def

    def set(self, key, *vals):
        """Set a named arguments to this node"""
        if len(vals) == 0:
            return self
        elif len(vals) > 1:
            return self.set(key, tuple(vals))
        # end if
        if key in self._kargs:
            self._kargs[key].set(vals[0])
        else:
            name = self.name + '_' + key
            self._kargs[key] = Node(vals[0], name=name)
        # end if
        return self
    # end def

# end class
