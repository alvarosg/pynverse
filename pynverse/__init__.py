__all__ = []


from .inverse import *
from .utils import *

from . import inverse
__all__ += inverse.__all__
del inverse

from . import utils
__all__ += utils.__all__
del utils


#from numpy.testing import Tester
#test = Tester().test

from numpy.testing import Tester
from numpy import test

def test(level=1, verbosity=1):
    from numpy.testing import Tester
    return Tester().test(level, verbosity)

if __name__ == "__main__":
    import doctest
    doctest.testmod()