from enum import Enum


class bc(Enum):
    PER = (0,)
    DIR = (1,)
    DIR_NEU = (2,)
    NEU_DIR = (3,)
    NEU = 4


def inverse_bc(bound):
    """return the inverse boundary condition"""
    if bound == bc.DIR:
        return bc.NEU
    if bound == bc.NEU:
        return bc.DIR
    if bound == bc.DIR_NEU:
        return bc.NEU_DIR
    if bound == bc.NEU_DIR:
        return bc.DIR_NEU
    return bc.PER


class direction(Enum):
    none = (0,)
    forward = (1,)
    backward = (2,)
    centered = 3


def inverse_dir(direct):
    """return the inverse direction"""
    if direct == direction.none:
        return direction.none
    if direct == direction.forward:
        return direction.backward
    if direct == direction.backward:
        return direction.forward
    return direction.centered
