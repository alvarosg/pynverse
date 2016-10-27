pynverse: A function that returns a callable that calculates the numerical inverse of the function `f` defined as an input callable. In its current form, it requires the function to be continuous in the real numbers, or in a predefined domain. Also, under those conditions, in order for the numerical inverse to exist in its domain, the input function must have strict monotonic (purely decreasing or purely increasing) behavior in that domain. By default the domain interval spans all the real numbers, however it can be restricted with the `domain` and `open_domain` arguments. The image of the function in the interval may be provided, for cases where the function is non continuous right at the end of an open interval.



Examples:
```
    >>> import scipy.misc
    >>> import numpy as np
    >>> cube = (lambda x: x**3)
    >>> invcube = scipy.misc.inversefunc(cube)
    >>> invcube(27) # Should give 3
    array(3.0000000063797567)

    >>> square = (lambda x: x**2)
    >>> invsquare = scipy.misc.inversefunc(square, domain=0)
    >>> invsquare([4, 16, 64]) # Should give [2, 4, 8]
    array([ 2.,  4.,  8.])

    >>> log = (lambda x: np.log10(x))
    >>> invlog = scipy.misc.inversefunc(log, domain=0, open_domain=True)
    >>> invlog(-2.) # Should give 0.01
    array(0.0099999999882423)

    >>> cos = (lambda x: np.cos(x))
    >>> invcos = scipy.misc.inversefunc(cos, domain=[0, np.pi])
    >>> invcos([1, 0, -1]) # Should give [0, pi / 2, pi]
    array([  5.44203736e-09,   1.57079632e+00,   3.14159265e+00])

    >>> tan = (lambda x: np.tan(x))
    >>> invtan = scipy.misc.inversefunc(tan,
    ...                                 domain=[-np.pi / 2, np.pi / 2],
    ...                                 open_domain=True)
    >>> invtan([1, 0, -1]) # Should give [pi / 4, 0, -pi / 4]
    array([  7.85398163e-01,   1.29246971e-26,  -7.85398163e-01])
```

Examples of using the callables with vectors to make plots, and compare to the analytical inverse:

![examples](https://cloud.githubusercontent.com/assets/12649253/19738042/cf22460a-9bad-11e6-9c17-6fdd6cda0991.png)

Each of those calculated as simply as:
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

Just to clarify, the main purpose of this function is not to be fast or to be as accurate as it could be if the inverse was calculated specifically for a known function. It is essentially a very user-friendly wrapper that uses the existing tools in scipy to solve the particular problem of finding the inverse of a function of those characteristics.
The good thing about this is that checking the result of the inverse function is as easy as checking that f(finv(x))==x, so even if the user inputs a non valid function, they can always make sure that the output is consistent or good enough, in fact the function checks this internally automatically. 
I see two type of users:
* Users who need a quick way to get the inverse of a function, so they do not have to invest time on doing it themselves. They could use it, check if the results, and if it does not work, then decide to invest the time to do it manually with more sophisticated approaches. Nevertheless for many cases this will be good enough (See examples above).
* Other functions that deal with monotonic functions, such as inverting cdf to ppf, or the normalization classes from matplotlib, which takes data intervals and map them linearly or non linearly to the 0-1 interval, using different non-linear functions. Essentially, any function that takes a callable of this characteristics, and may need at any point the inverse function, could very easily make use of this numerical approximation of the inverse.


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
