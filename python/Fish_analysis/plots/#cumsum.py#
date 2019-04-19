import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors, ticker, cm
import numpy as np
import sys
from matplotlib import cm
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

renorm = True
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
#evals, evecs, sum
evalsDTEy, evecsDTEy = np.linalg.eig(Dcov_20_1_TE_y) ; idxDTEy = evalsDTEy.argsort()[::1] ; evalsDTEy = evalsDTEy[idxDTEy] ; evecsDTEy = evecsDTEy[:,idxDTEy]
evalsGTEy, evecsGTEy = np.linalg.eig(Gcov_20_1_TE_y) ; idxGTEy = evalsGTEy.argsort()[::1] ; evalsGTEy = evalsGTEy[idxGTEy] ; evecsGTEy = evecsGTEy[:,idxGTEy]

#Plots
fig = plt.figure(figsize = (10,10))
plt.plot(1 + np.arange(20), np.cumsum(1/evalsDTEy)/np.sum(1/evalsDTEy), label = r'Decaying')
plt.plot(1 + np.arange(20), np.cumsum(1/evalsGTEy)/np.sum(1/evalsGTEy), label = r'Growing')
plt.text(x=18, y=0.92, s='0.95', color='gray', fontsize = 26)
plt.axhline(0.95, ls = '--', color = 'gray')
plt.xticks(1+np.arange(20))
plt.ylabel(r"$y_{\alpha_i}$", fontsize = 35)
plt.xlabel(r"Principal component", fontsize = 26)
plt.tick_params('both', labelsize = 30)
#plt.yscale('log')
plt.ylim([0.5,1.01])
plt.xlim([1,20])

plt.legend(frameon = False, fontsize = 26)
if renorm == False :
    plt.savefig("cumsum.pdf")
if renorm == True :
    plt.savefig("cumsum_R.pdf")
plt.show()
