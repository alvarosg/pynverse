from pynverse import inversefunc, piecewise

import numpy as np
import matplotlib.pyplot as plt
import scipy

cube = lambda x: x**3
invcube = inversefunc(cube)
invcube_a = lambda x: scipy.special.cbrt(x)

square = lambda x: x**2
invsquare = inversefunc(square, domain=0)
invsquare_a = lambda x: x**(1/2.)

log = lambda x: np.log10(x)
invlog = inversefunc(log, domain=0, open_domain=True)
invlog_a = lambda x: 10**x

cos = lambda x: np.cos(x)
invcos = inversefunc(cos, domain=[0, np.pi])
invcos_a = lambda x: np.arccos(x)

tan = lambda x: np.tan(x)
invtan = inversefunc(tan, 
                                domain=[-np.pi/2,np.pi/2],
                                open_domain=True)
invtan_a =lambda x: np.arctan2(x,1) 

pw=lambda x: piecewise(x,[x<1,(x>=1)*(x<3),x>=3],[lambda x: x, lambda x: x**2, lambda x: x+6])
invpw =inversefunc(pw) 
invpw_a=lambda x: piecewise(x,[x<1,(x>=1)*(x<9),x>=9],[lambda x: x, lambda x: x**0.5, lambda x: x-6])


N=50

def plot(title,ax1,x1,y1,ax2,x2,y21,y22):
    ax1.plot(x1,y1,'-')
    ax2.plot(x2,y22,'-',color='b')
    ax2.plot(x2,y21,'--',color='r')
    ax1.set_ylabel(title)


fig,axes=plt.subplots(6,2,figsize=(5,15))
x1=np.linspace(0,4,100)
x2=np.linspace(0,16,100)
plot('square',axes[0][0],x1,square(x1) ,axes[0][1],x2,invsquare_a(x2),invsquare(x2))
axes[0][1].legend(['Numerically','Analytical\nsolution'],fontsize=10,loc=4)
axes[0][1].set_title('Inverse functions')
axes[0][0].set_title('Direct functions')

x1=np.linspace(-2,2,100)
x2=np.linspace(-8,8,100)
plot('cube',axes[1][0],x1,cube(x1) ,axes[1][1],x2,invcube_a(x2),invcube(x2))

x1=np.linspace(0.00001,10,100)
x2=np.linspace(-5,1,100)
plot('log10',axes[2][0],x1,log(x1) ,axes[2][1],x2,invlog_a(x2),invlog(x2))

x1=np.linspace(0, np.pi,100)
x2=np.linspace(-1,1,100)
plot('cos',axes[3][0],x1,cos(x1) ,axes[3][1],x2,invcos_a(x2),invcos(x2))

x1=np.linspace(-np.pi/2+0.1, np.pi/2-0.1,100)
x2=np.linspace(-10,10,100)
plot('tan',axes[4][0],x1,tan(x1) ,axes[4][1],x2,invtan_a(x2),invtan(x2))

x1=np.linspace(0,4,100)
x2=np.linspace(0,10,100)
plot('piecewise',axes[5][0],x1,pw(x1) ,axes[5][1],x2,invpw_a(x2),invpw(x2))


plt.show()