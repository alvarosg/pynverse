# pynverse [![PyPI version](https://badge.fury.io/py/pynverse.svg)](https://badge.fury.io/py/pynverse)

A module specialized on calculating the numerical inverse of any invertible function.


## Requirements

  ![Scipy](https://img.shields.io/badge/scipy-%3E=0.11-blue.svg)
  ![Numpy](https://img.shields.io/badge/numpy-%3E=1.6-blue.svg)

## Install

In order to install this tool you'll need `pip`:

    pip install pynverse
    
## Usage

Pynverse provides a central function `inversefunc` that calculates the numerical inverse of a function `f` passed as the first argument in the form of a callable. 
```python
    >>> from pynverse import inversefunc
```

It can be used to calculate the inverse function at certain `y_values` points:
```python
    >>> cube = (lambda x: x**3)
    >>> invcube = inversefunc(cube, y_values=3)
    array(3.0000000063797567)
```

Or to obtain a callable that will calculate the inverse values at any other points if `y_values` is not provided:
```python
    >>> invcube = inversefunc(cube)
    >>> invcube(27)
    array(3.0000000063797567)
```

It requires the function to be continuous and strictly monotonic (i.e. purely decreasing or purely increasing) within the domain of the function. By default, the domain includes all real numbers, but it can be restricted to an inverval using the `domain` argument:
```python
    >>> import numpy as np
    >>> inversefunc(np.cos, y_values=[1, 0, -1], # Should give [0, pi / 2, pi]
    ...             domain=[0, np.pi])
    array([ 0.        ,  1.57079632,  3.14159265])
```

Additionally, the argument `open_domain` can be used to specify the open/closed characters of the end of the domain interval on one side:
```python
    >>> inversefunc(np.log10, y_values=-2, # Should give 0.01
    ...             domain=0, open_domain=[True, False])
    array(0.0099999999882423)
```

Or on both sides:
```python
    >>> invtan = inversefunc(np.tan,
    ...                      domain=[-np.pi / 2, np.pi / 2],
    ...                      open_domain=True)
    >>> invtan([1, 0, -1]) # Should give [pi / 4, 0, -pi / 4]
    array([  7.85398163e-01,   1.29246971e-26,  -7.85398163e-01])
```

Additional parameters may be passed to the function for easier reusability using the `args` argument:

```python
    >>> invsquare = inversefunc(np.power, args=(2), domain=0)
    >>> invsquare([4, 16, 64])
    array([ 2.,  4.,  8.])
```

The image of the function in the interval may be also provided for cases where the function is non continuous right at the end of an open interval with the `image` argument:

```python
    >>> invmod = inversefunc(np.mod, args=(1), domain=[5,6], 
    ...                      open_domain=[False,True], image=[0,1])
    >>> invmod([0.,0.3,0.5])
    array([ 5. ,  5.3,  5.5])
```

Additionally an argument can be used to check for the number of digis of accuracy of the results. Giving a warning in case it is not meet:
```python
    >>> inversefunc(np.log10, y_values=-8, # Should give 0.01
    ...             domain=0, open_domain=True, accuracy=6)
    pynverse\inverse.py:195: RuntimeWarning: Results obtained with less than 6 decimal digits of accuracy
    array(9.999514710830838e-09)
```

As it is compatible with arrays, it can very easily used to obtain the inverse for broad ranges. These are some examples of using the callables with vectors to make plots, and compare to the analytical inverse, each of them calculated as simply as:
```python
log = lambda x: np.log10(x)
invlog = scipy.misc.inversefunc(log, domain=0, open_domain=True)
x1=np.linspace(0.00001,10,100)
x2=np.linspace(-5,1,100)
ax1.plot(x1,log(y1),'b-')
ax2.plot(x2,invlog(x2),'b-')

invlog_a = lambda x: 10**x
ax2.plot(x2,invlog_a(x2),'r--')
```

![examples](https://cloud.githubusercontent.com/assets/12649253/19738042/cf22460a-9bad-11e6-9c17-6fdd6cda0991.png)

In particular, for the piecewise function case, there is a util funtion provided call `piecewise` that solves the issues of np.piecewise in order to make it work for both scalar and arrays. The functions for the last example were obtained as:

```python
from pynverse import inversefunc, piecewise

pw=lambda x: piecewise(x,[x<1,(x>=1)*(x<3),x>=3],[lambda x: x, lambda x: x**2, lambda x: x+6])
invpw =inversefunc(pw) 
invpw_a=lambda x: piecewise(x,[x<1,(x>=1)*(x<9),x>=9],[lambda x: x, lambda x: x**0.5, lambda x: x-6])
```

## Disclaimer

Just to clarify, the problem of calculating the numerical inverse of an arbitrary funtion in unlimited or open intervals, is still an open question in applied maths. The main purpose of this package is not to be fast, or as accurate as it could be if the inverse was calculated specifically for a known function, using more specialised techniques. The current implementation essentially uses the existing tools in scipy to solve the particular problem of finding the inverse of a function meeting the continuity and monotonicity conditions, but while it performs really well it may fail under certain conditions. For example when inverting a `log10` it is known to start giving inccacurate values when being asked to invert -10, which should correspond to 0.0000000001 (1e-10), but gives instead 0.0000000000978 (0.978e-10). 

The advantage about estimating the inverse function is that the accuracy can be verified by checking if f(finv(x))==x.. 

## Details about the implementation

The summarized internal strategy is the following:

0. Homogenize and normalize the input parameters.
1. Figure out if the function is increasing or decreasing. For this two reference points ref1 and ref2are need:
  - In a case of a closed interval, the points can 1/4 and 3/4 through the interval.
  - In an open interval any two values would work really.
  - if f(ref1)<(ref2), the function is increasing, otherwise is decreasing.
2. Figure out the image of the function in the interval. 
  - If the user gives values, then those are used.
  - In a closed interval just calculate f(a) and f(b).
  - In a closed interval try to calculate f(a) and f(b), if this works those are used. other wise it will be assume to be (-Inf, Inf).
3. I build a function the following function:
  -bounded_f(x):
    -return -Inf if x below interval, and f is increasing.
    -return +Inf if x below interval, and f is decreasing.
    -return +Inf if x above interval, and f is increasing.
    -return -Inf if x above interval, and f is decreasing.
    -return f(x) otherwise
4. If the required number y0 for the inverse is outside the image, raise an exception.
5. I find roots for bounded_f(x)-y0, by minimizing (bounded_f(x)-y0)**2, using the `Brent` method, making sure that the algorithm for minimising starts in a point inside the original interval by setting ref1, ref2 as brackets. As soon as if goes outside the allowed intervals, bounded_f will return infinite, forcing the algorithm to go back to search inside the interval. This could be further improved, although the current performance, is quite good already.
6. Check that the solutions are accurate and they meet f(x0)=y0 to some desired precision, raising a warning otherwise. 
