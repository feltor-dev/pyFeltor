def dot( matrix, vector):
    """ (matrix.dot(vector.flatten())).reshape(vector.shape) """
    return (matrix.dot(vector.flatten())).reshape(vector.shape)

