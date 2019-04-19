import matplotlib.pyplot as plt
import numpy as np

kmax = 1
kmin = -4
numks = 20
ks_arr = np.logspace(kmin, kmax, numks)
#TEdata = np.load("fish_%i_log.npy" %numks)
#Tdata = np.load("TT_fish_%i_log.npy" %numks)

TEdata = np.load("full_fish_d_%i.npy" %numks)
Tdata = np.load("TT_fish_d_%i.npy" %numks)

### Diag Fisher ###

plt.loglog(ks_arr, np.diag(TEdata), label = 'T+E')
plt.loglog(ks_arr, np.diag(Tdata), label = 'T')
plt.xlabel(r"k(Mpc^${-1}$)")
plt.ylabel(r"$F_{diag}$")
plt.title("Number of logarithmic bins = %i" %numks)
plt.legend()
#plt.savefig("Fdiag_%i_log.pdf" %numks)
plt.show()
