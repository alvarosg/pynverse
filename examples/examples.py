from pynverse import inversefunc


import numpy as np
cube = lambda x: x**3
invcube = inversefunc(cube)
print(invcube(27))


square = lambda x: x**2
invsquare = inversefunc(square, domain=0)
print(invsquare([4,16,64]))

log = lambda x: np.log10(x)
invlog = inversefunc(log, domain=0, open_domain=True)
print(invlog(-2.))

cos = lambda x: np.cos(x)
invcos = inversefunc(cos, domain=[0, np.pi])
print(invcos([1,0,-1]))



tan = lambda x: np.tan(x)
invtan = inversefunc(tan, 
                                domain=[-np.pi/2,np.pi/2],
                                open_domain=True)
print(invtan([1,0,-1]))
