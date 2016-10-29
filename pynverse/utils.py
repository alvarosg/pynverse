import numpy as np

__all__ = ['piecewise']

def piecewise(x, condlist, *args, **kwargs):
    x = np.asarray(x)
    shape = x.shape
    x = x.flatten()
    condlist = [np.asarray(c).flatten() for c in condlist]
    xout = np.piecewise(x, condlist, *args, **kwargs)
    return xout.reshape(shape)
