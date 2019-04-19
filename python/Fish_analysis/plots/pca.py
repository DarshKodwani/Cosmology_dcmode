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
    idx = evals.argsort()[::-1] #-1 for ordering highest value first, +1 for opposite
    evals = evals[idx]
    evecs = evecs[:,idx]
    return evals, evecs

evalsDTEy, evecsDTEy = cov_to_order_eigen(Dcov_20_1_TE_y)
evalsGTEy, evecsGTEy = cov_to_order_eigen(Gcov_20_1_TE_y) 

"""
fig, ax = plt.subplots(figsize = (12,10))
for index in range(0,4):
    ax.plot(ks_power, evalsDTEy[index]*evecsDTEy[:, index], label = r'Decaying')
    ax.plot(ks_power, evalsGTEy[index]*evecsGTEy[:, index], label = r'Growing')
    ax.set_xlabel(r"k \ Mpc$^{-1}$", fontsize = 15)
#    ax.ylabel(r"$\sigma_%i e_%i$" %(index+1, index+1), fontsize = 15)
#    ax[0,0].legend(fontsize = 20)    
    ax.set_title(r'Principle component %i' %(index+1), fontsize = 17)
    ax.tick_params('both', labelsize = 15)
#    ax.set_yscale('log')
plt.show()
"""

#print(evalsDTEy)
#print(evecsDTEy[0])
#quit()
fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (12,10))
axs = (ax[0,0], ax[0,1], ax[1,0], ax[1,1])
for index in range(0,4) :
    axs[index].plot(ks_power, evecsDTEy[:,index], label = r'Decaying')
    axs[index].plot(ks_power, evecsGTEy[:,index], label = r'Growing')
    axs[index].set_xlabel(r"k \ Mpc$^{-1}$", fontsize = 15)
    axs[index].set_ylabel(r"$\sigma_%i e_%i$" %(index+1, index+1), fontsize = 15)
    axs[index].set_xscale('log')
#    axs[index].set_yscale('log')
    axs[index].set_title(r'Principle component %i' %(index+1), fontsize = 17)
    axs[index].tick_params('both', labelsize = 15)
#    axs[index].set_xlim([0.,0.355])
    ax[0,0].legend(fontsize = 20)    

plt.tight_layout()
if renorm == True :
    plt.savefig("pca_R.pdf")
elif renorm == False :
    plt.savefig("pca.pdf")
plt.show()
