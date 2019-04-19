import matplotlib.pyplot as plt
import numpy as np

kmax = 1e1
kmin = 1e-4
numks = 20
ks_arr = np.linspace(kmin, kmax, numks)
TEdata = np.load("fish_%i_lin.npy" %numks)
Tdata = np.load("TT_fish_%i_lin.npy" %numks)

### Diag Fisher ###

plt.loglog(ks_arr, np.diag(TEdata), label = 'T+E')
plt.loglog(ks_arr, np.diag(Tdata), label = 'T')
plt.xlabel(r"k(Mpc^${-1}$)")
plt.ylabel(r"$F_{diag}$")
plt.title("Number of linear bins = %i" %numks)
plt.legend()
plt.savefig("Fdiag_%i_log.pdf" %numks)
plt.show()
quit()
### Full Fisher ###
CS = plt.contour(ks_arr, ks_arr, data, 1000)
cbar = plt.colorbar(CS)
#plt.imshow(data)
plt.yscale('log')
plt.xscale('log')
plt.show()
