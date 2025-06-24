import numpy as np


def delta(n):
    op = np.zeros((n, n))
    for i in range(0, n):
        op[i, i] = 1.0
    return op


def pipj(n):
    op = np.zeros((n, n))
    for i in range(0, n):
        op[i, i] = 2.0 / (2 * i + 1.0)
    return op


def pipj_inv(n):
    op = np.zeros((n, n))
    for i in range(0, n):
        op[i, i] = (2 * i + 1.0) / 2.0
    return op


def pidxpj(n):
    op = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            if (i < j) and ((i + j) % 2 != 0):
                op[i, j] = 2
    return op


def rirj(n):
    op = np.zeros((n, n))
    op.fill(1)
    return op


def rilj(n):
    op = np.zeros((n, n))
    op.fill(-1)
    for i in range(0, n):
        for j in range(0, n):
            if j % 2 == 0:
                op[i, j] = 1.0
    return op


def lirj(n):
    op = rilj(n)
    return np.transpose(op)


def lilj(n):
    op = np.zeros((n, n))
    op.fill(-1)
    for i in range(0, n):
        for j in range(0, n):
            if ((i + j) % 2) == 0:
                op[i, j] = 1.0
    return op


def ninj(n):
    op = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            if i == j + 1:
                op[i, j] = 2.0 / (2 * i + 1) / (2 * j + 1)
            if i == j - 1:
                op[i, j] = -2.0 / (2 * i + 1) / (2 * j + 1)
    op[0, 0] = 2
    return op


def backward(n):
    (x, w) = np.polynomial.legendre.leggauss(n)
    vander = np.polynomial.legendre.legvander(x, n - 1)
    return vander


def forward(n):
    vander = backward(n)
    return np.linalg.inv(vander)
