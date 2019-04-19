import numpy as np 
import matplotlib.pyplot as plt

crosst = np.loadtxt("decay_testscls_ten_addct.dat")
growt = np.loadtxt("decay_testsclt.dat")
decayt = np.loadtxt("decay_testscl_addct.dat")

ells = growt[:,0]
gt_BB = growt[:,4]
dt_BB = decayt[:,4]
gdt_BB = crosst[:,4]

ell_factor = ells*(ells+1)
plt.loglog(ells, ell_factor*gt_BB, label = 'grow')
plt.loglog(ells, ell_factor*dt_BB, label = 'decay')
plt.loglog(ells, ell_factor*gdt_BB, label = 'cross')
plt.legend()
plt.show()

