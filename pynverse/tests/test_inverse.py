import numpy as np
from numpy.testing import (assert_array_equal, assert_almost_equal,
                           assert_array_almost_equal, assert_equal, assert_)

from pynverse import inversefunc


def test_inversefunc_infinite():
    accuracy = 2
    cube = (lambda x: x**3)
    invfunc = inversefunc(cube)
    yval = [-27, -8, -1, 0, 1, 8, 27]
    xvalexpected = [-3, -2, -1, 0, 1, 2, 3]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vminclosed():
    accuracy = 2
    square = (lambda x: x**2)
    invfunc = inversefunc(square, domain=0)
    yval = [4, 16, 64]
    xvalexpected = [2, 4, 8]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vminopen():
    accuracy = 2
    log = (lambda x: np.log10(x))
    invfunc = inversefunc(log, domain=0,
                          open_domain=True,
                          image=[-np.inf, None])
    yval = [-2., -3.]
    xvalexpected = [0.01, 0.001]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vmaxclosed():
    accuracy = 2
    square = (lambda x: x**2)
    invfunc = inversefunc(square, domain=[None, 0])
    yval = [4, 16, 64]
    xvalexpected = [-2, -4, -8]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vmaxopen():
    accuracy = 2
    log = (lambda x: np.log10(-x))
    invfunc = inversefunc(log, domain=[None, 0],
                          open_domain=True,
                          image=[-np.inf, None])
    yval = [-2., -3.]
    xvalexpected = [-0.01, -0.001]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vminclosedvmaxclosed():
    accuracy = 2
    cos = (lambda x: np.cos(x))
    invfunc = inversefunc(cos, domain=[0, np.pi])
    yval = [1, 0, -1]
    xvalexpected = [0., np.pi / 2, np.pi]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vminopenvmaxclosed():
    accuracy = 2
    cos = (lambda x: np.cos(x))
    invfunc = inversefunc(cos, domain=[0, np.pi], open_domain=[True, False])
    yval = [1 / np.sqrt(2), 0, -1 / np.sqrt(2)]
    xvalexpected = [np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vminclosedvmaxopen():
    accuracy = 2
    cos = (lambda x: np.cos(x))
    invfunc = inversefunc(cos, domain=[0, np.pi], open_domain=[False, True])
    yval = [1 / np.sqrt(2), 0, -1 / np.sqrt(2)]
    xvalexpected = [np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_vminopenvmaxopen():
    accuracy = 2
    tan = (lambda x: np.tan(x))
    invfunc = inversefunc(tan,
                          domain=[-np.pi / 2, np.pi / 2],
                          open_domain=True)
    yval = [1, 0, -1]
    xvalexpected = [np.pi / 4, 0., -np.pi / 4]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_with_y_values():
    accuracy = 2
    cube = (lambda x: x**3)
    yval = [-27, -8, -1, 0, 1, 8, 27]
    xvalexpected = [-3, -2, -1, 0, 1, 2, 3]
    xval = inversefunc(cube, y_values=yval)
    assert_array_almost_equal(xval, xvalexpected, accuracy)

def test_inversefunc_with_args():
    accuracy = 2
    invfunc = inversefunc(np.power, args=3)
    yval = [-27, -8, -1, 0, 1, 8, 27]
    xvalexpected = [-3, -2, -1, 0, 1, 2, 3]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)

def test_inversefunc_with_multargs():
    accuracy = 2
    func = (lambda x, y, z: x**3 + y + z)
    invfunc = inversefunc(func, args=(1, 2))
    yval = [-24, -5, 2, 3, 4, 11, 30]
    xvalexpected = [-3, -2, -1, 0, 1, 2, 3]
    assert_array_almost_equal(invfunc(yval), xvalexpected, accuracy)
