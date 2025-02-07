from argparse import Namespace

import numpy as np

NN= -999999  # No Number, a trick to aovid nans in data structs

class Counters(Namespace):

    def set(self, **kwds):
        for name, value in kwds.items():
            setattr(self, name, value)

    def init(self, **kwds):
        for name, value in kwds.items():
            assert name not in self
            setattr(self, name, value)


class xy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def pos(self): return np.stack(([self.x], [self.y]), axis=1)

    @property
    def XY(self): return (self.x, self.y)

    @property
    def X(self): return self.x

    @property
    def Y(self): return self.y

    @property
    def R(self): return np.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def Phi(self): return np.arctan2(self.y, self.x)

    def __str__(self):
        return 'xy(x={.x}, y={.y})'.format(self, self)
    __repr__ = __str__

    def __getitem__(self, n):
        if n == 0: return self.x
        if n == 1: return self.y
        raise IndexError


class minmax:

    def __init__(self, min, max):
        assert min <= max
        self.min = min
        self.max = max

    @property
    def bracket(self): return self.max - self.min

    @property
    def interval(self): return (self.min, self.max) 

    @property
    def center(self): return (self.max + self.min) / 2

    def contains(self, x):
        return self.min <= x < self.max

    def __mul__(self, factor):
        return minmax(self.min * factor, self.max * factor)

    def __truediv__(self, factor):
        assert factor != 0
        return self.__mul__(1./factor)

    def __add__(self, scalar):
        return minmax(self.min + scalar, self.max + scalar)

    def __sub__(self, scalar):
        return minmax(self.min - scalar, self.max - scalar)

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max

    def __str__(self, decimals=None):
        if decimals is None:
            return 'minmax(min={.min}, max={.max})'.format(self, self)
        fmt = 'minmax(min={{.min:.{0}f}}, max={{.max:.{0}f}})'.format(decimals)
        return fmt.format(self, self)
    __repr__ = __str__

    def __getitem__(self, n):
        if n == 0: return self.min
        if n == 1: return self.max
        raise IndexError
