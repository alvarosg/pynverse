# pynverse [![PyPI version](https://badge.fury.io/py/pynverse.svg)](https://badge.fury.io/py/pynverse)

A module specialized on calculating the numerical inverse of any invertible continuous function.


## Requirements

  ![Scipy](https://img.shields.io/badge/scipy-%3E=0.11-blue.svg)
  ![Numpy](https://img.shields.io/badge/numpy-%3E=1.6-blue.svg)

## Install

In order to install this tool you'll need `pip`:

    pip install git+git://github.com/alvarosg/pynverse.git
    
Note installing from PyPI is not longer supported / maintained.
    
## Usage

Pynverse provides a main function `inversefunc` that calculates the numerical inverse of a function `f` passed as the first argument in the form of a callable. 
```python
    >>> from pynverse import inversefunc
```

It can be used to calculate the inverse function at certain `y_values` points:
```python
    >>> cube = (lambda x: x**3)
    >>> invcube = inversefunc(cube, y_values=27)
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

Additionally, the argument `open_domain` can be used to specify the open/closed character of each of the ends of the domain interval:
```python
    >>> inversefunc(np.log10, y_values=-2, # Should give 0.01
    ...             domain=0, open_domain=[True, False])
    array(0.0099999999882423)
```

Or on both ends simultaneously:
```python
    >>> invtan = inversefunc(np.tan,
    ...                      domain=[-np.pi / 2, np.pi / 2],
    ...                      open_domain=True)
    >>> invtan([1, 0, -1]) # Should give [pi / 4, 0, -pi / 4]
    array([  7.85398163e-01,   1.29246971e-26,  -7.85398163e-01])
```

Additional parameters may be passed to the function for easier reusability of callables using the `args` argument:

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

Additionally an argument can be used to check for the number of digits of accuracy in the results, giving a warning in case this is not meet:
```python
    >>> inversefunc(np.log10, y_values=-8, # Should give 0.01
    ...             domain=0, open_domain=True, accuracy=6)
    pynverse\inverse.py:195: RuntimeWarning: Results obtained with less than 6 decimal digits of accuracy
    array(9.999514710830838e-09)
```

As it is compatible with arrays, it can very easily used to obtain the inverse for broad ranges. These are some examples of using the returned numerical inverse callables with arrays to make plots, and compare them to the analytical inverse, each of them calculated as simply as:
```python
log = lambda x: np.log10(x)
invlog = inversefunc(log, domain=0, open_domain=True)
x1=np.linspace(0.00001,10,100)
x2=np.linspace(-5,1,100)
ax1.plot(x1,log(y1),'b-')
ax2.plot(x2,invlog(x2),'b-')

invlog_a = lambda x: 10**x
ax2.plot(x2,invlog_a(x2),'r--')
```

![](https://cloud.githubusercontent.com/assets/12649253/19738042/cf22460a-9bad-11e6-9c17-6fdd6cda0991.png)

In particular, for the definition of piecewise functions, there is a `piecewise` utility function provided that solves the issues of np.piecewise when working with both scalars and arrays. For example, the inverse for the last plot was obtained as:

```python
from pynverse import inversefunc, piecewise

pw=lambda x: piecewise(x,[x<1,(x>=1)*(x<3),x>=3],
                       [lambda x: x, lambda x: x**2, lambda x: x+6])
invpw =inversefunc(pw) 
```

## Disclaimer

The problem of calculating the numerical inverse of an arbitrary function in unlimited or open intervals is still an open question in applied mathematics. The main purpose of this package is not to be fast, or as accurate as it could be if the inverse was calculated specifically for a known function, using more specialised techniques. The current implementation essentially uses the existing tools in scipy to solve the particular problem of finding the inverse of a function meeting the continuity and monotonicity conditions, but while it performs really well it may fail under certain conditions. For example when inverting a `log10` it is known to start giving inccacurate values when being asked to invert -10, which should correspond to 0.0000000001 (1e-10), but gives instead 0.0000000000978 (0.978e-10). 

The advantage about estimating the inverse function is that the accuracy can always be verified by checking if f(finv(x))==x.

## Details about the implementation

The summarized internal strategy is the following:

1. Figure out if the function is increasing or decreasing. For this two reference points ref1 and ref2 are needed:
    * In case of a finite interval, the points ref points are 1/4 and 3/4 through the interval.
    * In an infinite interval any two values work really.
    * If f(ref1)<f(ref2), the function is increasing, otherwise is decreasing.
2. Figure out the image of the function in the interval. 
    * If values are provided, then those are used.
    * In a closed interval just calculate f(a) and f(b), where a and b are the ends of the interval.
    * In an open interval try to calculate f(a) and f(b), if this works those are used, otherwise it will be assume to be (-Inf, Inf).
3. Built a bounded function with the following conditions:
    * bounded_f(x):
        * return -Inf if x below interval, and f is increasing.
        * return +Inf if x below interval, and f is decreasing.
        * return +Inf if x above interval, and f is increasing.
        * return -Inf if x above interval, and f is decreasing.
        * return f(x) otherwise
4. If the required number y0 for the inverse is outside the image, raise an exception.
5. Find roots for bounded_f(x)-y0, by minimizing (bounded_f(x)-y0)**2, using the `Brent` method, making sure that the algorithm for minimising starts in a point inside the original interval by setting ref1, ref2 as brackets. As soon as if goes outside the allowed intervals, bounded_f returns infinite, forcing the algorithm to go back to search inside the interval.
6. Check that the solutions are accurate and they meet f(x0)=y0 to some desired precision, raising a warning otherwise. 
