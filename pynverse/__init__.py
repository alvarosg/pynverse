__all__ = []


from .version import version as __version__

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