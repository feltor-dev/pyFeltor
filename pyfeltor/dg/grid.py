# n[0] corresponds to the leftmost dimension
# x corresponds to the rightmost dimension (the fastest varying in memory)
# Dimension is given by  length of parameters
import numpy as np


class Grid:
    def __init__(self, x0, x1, n, N, bc):
        """Create from lists of same length, which is the dimension of the grid"""
        assert (
            (len(x0) == len(x1))
            and (len(x0) == len(n))
            and (len(x0) == len(N))
            and (len(x0) == len(bc))
        )
        self.x0 = np.asarray(x0)  # must be numpy array of length dimension
        self.x1 = np.asarray(x1)  # lengths must be consistent
        self.n = np.asarray(n)
        self.N = np.asarray(N)
        self.bc = bc

    @property
    def n(self):
        return self.__n

    @property
    def N(self):
        return self.__N

    @property
    def x0(self):
        return self.__x0

    @property
    def x1(self):
        return self.__x1

    @property
    def bc(self):
        return self.__bc

    @property
    def ndim(self):
        """Return the number of dimensions in the grid"""
        return len(self.x0)

    @n.setter
    def n(self, n):
        self.__n = np.asarray(n)

    @N.setter
    def N(self, N):
        self.__N = np.asarray(N)

    @x0.setter
    def x0(self, x0):
        self.__x0 = np.asarray(x0)

    @x1.setter
    def x1(self, x1):
        self.__x1 = np.asarray(x1)

    @bc.setter
    def bc(self, bc):
        self.__bc = bc

    def lx(self):
        return self.x1 - self.x0

    def h(self):
        return (self.x1 - self.x0) / self.N

    # should this be named shape? (consistent with both feltor and numpy?)
    def size(self):  # makes the shape of numpy arrays
        return self.n * self.N
