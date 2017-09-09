# -*- coding: utf-8 -*-
"""Unlicensed"""
from collections import OrderedDict
from .executor import Execute

class Node:
    """Node is a independent unit that holds some data or a function"""

    def __init__(self, data, name=None):
        self._args = []
        self._kargs = OrderedDict()
        self.name = name
        self._set_id()
        self.data = data
        self.result = None
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

    def _set_id(self):
        self._id += 1
        self.__id__ = self._id
        if not self.name:
            self.name = 'Node_' + self._id
        # end if
    # end if

    def get(self, key == None):
        """Get a named argument"""
        if key is None:
            return self.execute()
        elif key in self._kargs:
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

    def execute(self):
        if self.result is not None:
            return self.result
        # end if
        self.result = execute(self)
        return self.result
    # end def

# end class
