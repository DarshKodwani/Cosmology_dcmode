import matplotlib.pyplot as plt
import numpy as np

kmax = 1
kmin = -4
numks = 20
ks_arr = np.logspace(kmin, kmax, numks)
mode = "g"

TEdata = np.load("full_fish_%s_%i.npy" %(mode,numks))
Tdata = np.load("TT_fish_%s_%i.npy" %(mode,numks))

### Diag Fisher ###

plt.loglog(ks_arr, np.diag(TEdata), label = 'T+E')
plt.loglog(ks_arr, np.diag(Tdata), label = 'T')
plt.xlabel(r"k(Mpc^${-1}$)")
plt.ylabel(r"$F_{diag}$")
plt.title("Number of bins = %i" %numks)
plt.legend()
plt.savefig("Fdiag_%s_%i.pdf" %(mode,numks))
plt.show()
