import numpy as np
import matplotlib.pyplot as plt



v =22.414   ##Volume molaire de l'hélium en L/mol
N=6.022e23

def operations(V):
    n=V/v * N
    return n*3          

def temps (V):
    operations(V)

V=np.linspace(0.01,1000,10000)
op=operations(V)

plt.plot(V,op)
plt.show()
