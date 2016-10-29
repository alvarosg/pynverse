__all__ = []

__version__ = '0.1.4'

from .inverse import *
from .utils import *

from . import inverse
__all__ += inverse.__all__
del inverse

from . import utils
__all__ += utils.__all__
del utils

if __name__ == "__main__":
    import doctest
    doctest.testmod()