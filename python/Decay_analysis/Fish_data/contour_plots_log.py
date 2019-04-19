import matplotlib.pyplot as plt
import numpy as np

kmax = 1
kmin = -4
numks = 20
ks_arr = np.logspace(kmin, kmax, numks)
TEdata = np.load("fish_%i_log.npy" %numks)
Tdata = np.load("TT_fish_%i_log.npy" %numks)

### Full Fisher ###
CS = plt.contour(ks_arr, ks_arr, TEdata, 1000)
cbar = plt.colorbar(CS)
plt.yscale('log')
plt.xscale('log')
#plt.imshow(np.log(TEdata))
plt.savefig("contour1_TE.pdf")
plt.show()
