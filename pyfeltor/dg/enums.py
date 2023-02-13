from enum import Enum

class bc(Enum):
    PER = 0,
    DIR = 1,
    DIR_NEU = 2,
    NEU_DIR = 3,
    NEU = 4

class direction(Enum):
    none = 0,
    forward = 1,
    backward = 2,
    centered = 3

