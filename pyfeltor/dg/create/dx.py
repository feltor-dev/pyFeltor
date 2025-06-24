import scipy.sparse

from ..enums import bc
from . import operators as ops


def symm(n, N, h, bcx):
    ll = ops.lilj(n)
    rr = ops.rirj(n)
    lr = ops.lirj(n)
    rl = ops.rilj(n)
    d = ops.pidxpj(n)
    t = ops.pipj_inv(n)
    t *= 2.0 / h

    a = 1.0 / 2.0 * t @ (d - d.transpose())  # @ is matrix multiplication
    # bcx = PER
    a_bound_right = a.copy()
    a_bound_left = a.copy()
    # left boundary
    if (bcx == bc.DIR) or (bcx == bc.DIR_NEU):
        a_bound_left += 0.5 * (t @ ll)
    elif (bcx == bc.NEU) or (bcx == bc.NEU_DIR):
        a_bound_left -= 0.5 * (t @ ll)
    # right boundary
    if (bcx == bc.DIR) or (bcx == bc.NEU_DIR):
        a_bound_right -= 0.5 * (t @ rr)
    elif (bcx == bc.NEU) or (bcx == bc.DIR_NEU):
        a_bound_right += 0.5 * (t @ rr)
    b = t @ (1.0 / 2.0 * rl)
    bp = t @ (-1.0 / 2.0 * lr)  # pitfall: T*-m^T is NOT -(T*m)^T
    # transform to XSPACE
    backward = ops.backward(n)
    forward = ops.forward(n)
    a = (backward @ a) @ forward
    b = (backward @ b) @ forward
    bp = (backward @ bp) @ forward
    a_bound_left = (backward @ a_bound_left) @ forward
    a_bound_right = (backward @ a_bound_right) @ forward
    # assemble the matrix
    rows = []
    cols = []
    vals = []
    if bcx != bc.PER:
        for i in range(0, n):
            for j in range(0, n):
                rows.append(0 * n + i)
                cols.append((0 * n + j) % (n * N))
                vals.append(a_bound_left[i, j])

                rows.append(0 * n + i)
                cols.append(((0 + 1) * n + j) % (n * N))
                vals.append(b[i, j])

        for k in range(1, N - 1):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append(((k - 1) * n + j) % (n * N))
                    vals.append(bp[i, j])

                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

                    rows.append(k * n + i)
                    cols.append(((k + 1) * n + j) % (n * N))
                    vals.append(b[i, j])

        for i in range(0, n):
            for j in range(0, n):
                rows.append((N - 1) * n + i)
                cols.append((((N - 1) - 1) * n + j) % (n * N))
                vals.append(bp[i, j])

                rows.append((N - 1) * n + i)
                cols.append(((N - 1) * n + j) % (n * N))
                vals.append(a_bound_right[i, j])

    else:  # periodic
        for k in range(0, N):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append(((k - 1) * n + j) % (n * N))
                    vals.append(bp[i, j])

                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

                    rows.append(k * n + i)
                    cols.append(((k + 1) * n + j) % (n * N))
                    vals.append(b[i, j])

    # sort
    rows, cols, vals = zip(*sorted(zip(rows, cols, vals, strict=False)), strict=False)
    return scipy.sparse.coo_matrix((vals, (rows, cols)))


def plus(n, N, h, bcx):
    ll = ops.lilj(n)
    #rr = ops.rirj(n)
    #lr = ops.lirj(n)
    rl = ops.rilj(n)
    d = ops.pidxpj(n)
    t = ops.pipj_inv(n)
    t *= 2.0 / h

    a = t @ (-ll - d.transpose())
    # bcx = PER
    a_bound_left = a.copy()  # PER, NEU, and NEU_DIR
    a_bound_right = a.copy()  # PER, DIR, and NEU_DIR
    if (bcx == bc.DIR) or (bcx == bc.DIR_NEU):
        a_bound_left = t @ (-d.transpose())
    if (bcx == bc.NEU) or (bcx == bc.DIR_NEU):
        a_bound_right = t @ d
    b = t @ rl
    # transform to XSPACE
    backward = ops.backward(n)
    forward = ops.forward(n)
    a = (backward @ a) @ forward
    b = (backward @ b) @ forward
    a_bound_left = (backward @ a_bound_left) @ forward
    a_bound_right = (backward @ a_bound_right) @ forward
    # assemble the matrix
    rows = []
    cols = []
    vals = []
    if bcx != bc.PER:
        for i in range(0, n):
            for j in range(0, n):
                rows.append(0 * n + i)
                cols.append((0 * n + j) % (n * N))
                vals.append(a_bound_left[i, j])

                rows.append(0 * n + i)
                cols.append(((0 + 1) * n + j) % (n * N))
                vals.append(b[i, j])

        for k in range(1, N - 1):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

                    rows.append(k * n + i)
                    cols.append(((k + 1) * n + j) % (n * N))
                    vals.append(b[i, j])

        for i in range(0, n):
            for j in range(0, n):
                rows.append((N - 1) * n + i)
                cols.append(((N - 1) * n + j) % (n * N))
                vals.append(a_bound_right[i, j])

    else:  # periodic
        for k in range(0, N):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

                    rows.append(k * n + i)
                    cols.append(((k + 1) * n + j) % (n * N))
                    vals.append(b[i, j])

    # sort
    rows, cols, vals = zip(*sorted(zip(rows, cols, vals, strict=False)), strict=False)
    return scipy.sparse.coo_matrix((vals, (rows, cols)))


def minus(n, N, h, bcx):
    ll = ops.lilj(n)
    #rr = ops.rirj(n)
    lr = ops.lirj(n)
    #rl = ops.rilj(n)
    d = ops.pidxpj(n)
    t = ops.pipj_inv(n)
    t *= 2.0 / h

    a = t @ (ll + d)
    # bcx = PER
    a_bound_right = a.copy()  # PER, NEU and DIR_NEU
    a_bound_left = a.copy()  # PER, DIR and DIR_NEU
    if (bcx == bc.DIR) or (bcx == bc.NEU_DIR):
        a_bound_right = t @ (-d.transpose())
    if (bcx == bc.NEU) or (bcx == bc.NEU_DIR):
        a_bound_left = t @ d
    bp = -t @ lr
    # transform to XSPACE
    backward = ops.backward(n)
    forward = ops.forward(n)
    a = (backward @ a) @ forward
    bp = (backward @ bp) @ forward
    a_bound_left = (backward @ a_bound_left) @ forward
    a_bound_right = (backward @ a_bound_right) @ forward
    # assemble the matrix
    rows = []
    cols = []
    vals = []
    if bcx != bc.PER:
        for i in range(0, n):
            for j in range(0, n):
                rows.append(0 * n + i)
                cols.append((0 * n + j) % (n * N))
                vals.append(a_bound_left[i, j])

        for k in range(1, N - 1):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append(((k - 1) * n + j) % (n * N))
                    vals.append(bp[i, j])

                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

        for i in range(0, n):
            for j in range(0, n):
                rows.append((N - 1) * n + i)
                cols.append((((N - 1) - 1) * n + j) % (n * N))
                vals.append(bp[i, j])

                rows.append((N - 1) * n + i)
                cols.append(((N - 1) * n + j) % (n * N))
                vals.append(a_bound_right[i, j])

    else:  # periodic
        for k in range(0, N):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append(((k - 1) * n + j) % (n * N))
                    vals.append(bp[i, j])

                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

    # sort
    rows, cols, vals = zip(*sorted(zip(rows, cols, vals, strict=False)), strict=False)
    return scipy.sparse.coo_matrix((vals, (rows, cols)))


def jump_normed(n, N, h, bcx):
    ll = ops.lilj(n)
    rr = ops.rirj(n)
    lr = ops.lirj(n)
    rl = ops.rilj(n)

    t = ops.pipj_inv(n)
    t *= 2.0 / h
    a = t @ (ll + rr)
    a_bound_left = a.copy()  # DIR and PER
    if (bcx == bc.NEU) or (bcx == bc.NEU_DIR):
        a_bound_left = t @ rr
    a_bound_right = a.copy()  # DIR and PER
    if (bcx == bc.NEU) or (bcx == bc.DIR_NEU):
        a_bound_right = t @ ll
    b = -t @ rl
    bp = -t @ lr
    # transform to XSPACE
    backward = ops.backward(n)
    forward = ops.forward(n)
    a = (backward @ a) @ forward
    b = (backward @ b) @ forward
    bp = (backward @ bp) @ forward
    a_bound_left = (backward @ a_bound_left) @ forward
    a_bound_right = (backward @ a_bound_right) @ forward
    # assemble the matrix
    rows = []
    cols = []
    vals = []
    if bcx != bc.PER:
        for i in range(0, n):
            for j in range(0, n):
                rows.append(0 * n + i)
                cols.append((0 * n + j) % (n * N))
                vals.append(a_bound_left[i, j])

                rows.append(0 * n + i)
                cols.append(((0 + 1) * n + j) % (n * N))
                vals.append(b[i, j])

        for k in range(1, N - 1):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append(((k - 1) * n + j) % (n * N))
                    vals.append(bp[i, j])

                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

                    rows.append(k * n + i)
                    cols.append(((k + 1) * n + j) % (n * N))
                    vals.append(b[i, j])

        for i in range(0, n):
            for j in range(0, n):
                rows.append((N - 1) * n + i)
                cols.append((((N - 1) - 1) * n + j) % (n * N))
                vals.append(bp[i, j])

                rows.append((N - 1) * n + i)
                cols.append(((N - 1) * n + j) % (n * N))
                vals.append(a_bound_right[i, j])

    else:  # periodic
        for k in range(0, N):
            for i in range(0, n):
                for j in range(0, n):
                    rows.append(k * n + i)
                    cols.append(((k - 1) * n + j) % (n * N))
                    vals.append(bp[i, j])

                    rows.append(k * n + i)
                    cols.append((k * n + j) % (n * N))
                    vals.append(a[i, j])

                    rows.append(k * n + i)
                    cols.append(((k + 1) * n + j) % (n * N))
                    vals.append(b[i, j])

    # sort
    rows, cols, vals = zip(*sorted(zip(rows, cols, vals, strict=False)), strict=False)
    return scipy.sparse.coo_matrix((vals, (rows, cols)))


def normed(n, N, h, bcx, direction):
    if direction == direction.centered:
        return symm(n, N, h, bcx)
    elif direction == direction.forward:
        return plus(n, N, h, bcx)
    elif direction == direction.backward:
        return minus(n, N, h, bcx)
