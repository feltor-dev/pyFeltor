import numpy as np


class Grid:
    def __init__(self, x0, x1, n, N):
        """Create from lists of same length, which is the dimension of the grid

        For the one-dimensional case numbers can be given which will be
        converted to lists
        Dimension is given by length of parameters
        """
        self.x0 = np.asarray(x0)
        try:
            len(x0)
        except TypeError:
            self.x0 = np.asarray([x0])

        self.x1 = np.asarray(x1)  # must be numpy array of length dimension
        try:
            len(x1)
        except TypeError:
            self.x1 = np.asarray([x1])
        self.n = np.asarray(n)  # must be numpy array of length dimension
        try:
            len(n)
        except TypeError:
            self.n = np.asarray([n])
        self.N = np.asarray(N)  # must be numpy array of length dimension
        try:
            len(N)
        except TypeError:
            self.N = np.asarray([N])
        # lengths must be consistent
        assert(len(self.x0) == len(self.x1))
        assert(len(self.x0) == len(self.n))
        assert(len(self.x0) == len(self.N))

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
    def ndim(self):
        """Return the number of dimensions in the grid"""
        return len(self.x0)

    @property
    def shape(self):
        """Shape of the grid : n*N"""
        return self.n * self.N

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

    def lx(self):
        return self.x1 - self.x0

    def h(self):
        return (self.x1 - self.x0) / self.N

    def size(self):
        """The total number of points in the grid: np.prod(grid.shape)"""
        return np.prod(self.shape)
