import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors, ticker, cm
import numpy as np
import sys
from matplotlib import cm
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

renorm = False
#Import ks

ks_arr = np.load("../Data/G_Data/karr_numks20.npy")
ks_full = ks_arr[0]
ks_bins = ks_arr[1]
ks_power = ks_full[ks_bins]

#Import fishers and compute cov

if renorm == False : 
    Dcov_20_1_TE_y = np.linalg.inv(np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseY.npy"))
elif renorm == True : 
    Dcov_20_1_TE_y = np.linalg.inv(np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseY_R.npy"))

Gcov_20_1_TE_y = np.linalg.inv(np.load("../Data/G_Data/fish_numks20_fsky1.00_TE_noiseY.npy"))

#PCA

def cov_to_order_eigen(cov) : 
    evals, evecs = np.linalg.eig(cov) 
    idx = evals.argsort()[::1] #-1 for ordering highest value first, +1 for opposite
    evals = evals[idx]
    evecs = evecs[:,idx]
    return evals, evecs

evalsDTEy, evecsDTEy = cov_to_order_eigen(Dcov_20_1_TE_y)
evalsGTEy, evecsGTEy = cov_to_order_eigen(Gcov_20_1_TE_y) 

fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (16,10))

for index in range(0,4):
    ax[0].plot(ks_power, evecsDTEy[:,index], label = r'PC %i, $e_%i$ = %.2E' %(index+1, index+1, evalsDTEy[index]))
    ax[0].set_title(r'Decaying mode principal components', fontsize = 24)
    ax[0].legend(fontsize = 16)
    ax[0].set_xlabel(r"k \ Mpc$^{-1}$", fontsize = 20)
    ax[0].tick_params('both', labelsize = 20)
    ax[1].plot(ks_power, evecsGTEy[:,index], label = r'PC %i, $e_%i$ = %.2E' %(index+1, index+1, evalsGTEy[index]))
    ax[1].set_title(r'Growing mode principal components', fontsize = 24)
    ax[1].legend(fontsize = 16)
    ax[1].set_xlabel(r"k \ Mpc$^{-1}$", fontsize = 20)
    ax[1].tick_params('both', labelsize = 20)

plt.tight_layout()
plt.savefig('pca_new.pdf')
plt.show()
