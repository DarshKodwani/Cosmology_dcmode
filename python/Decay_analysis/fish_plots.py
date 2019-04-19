import numpy as np
import matplotlib.pyplot as plt

#Universal params#

kmax = 1
kmin = -4
numks = 50
ks_arr = np.logspace(kmin, kmax, numks)

#Plotting

fish = np.load("Fish_data/fish_%i.npy" %numks)


plt.imshow(fish)
#plt.plot(ks_arr, np.diag(fish))
plt.show()
