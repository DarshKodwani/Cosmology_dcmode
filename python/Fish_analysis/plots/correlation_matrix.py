import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors, ticker, cm
import numpy as np
import sys
from matplotlib.font_manager import FontProperties
from matplotlib import cm
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

mode = "D"
renorm = True

#Import ks

ks_arr = np.load("../Data/G_Data/karr_numks20.npy")
ks_full = ks_arr[0]
ks_bins = ks_arr[1]
ks_power = ks_full[ks_bins]

#Import fishers and compute cov

def corr_matrix(cov) : 
    corr = np.zeros([len(ks_power), len(ks_power)])
    for i in range(len(ks_power)) : 
        for j in range(len(ks_power)) : 
            corr[i,j] = cov[i,j]/(np.sqrt(cov[i,i])*np.sqrt(cov[j,j]))
            if j != i : 
                corr[j,i] = corr[i,j]
    return corr

fig, ax = plt.subplots(figsize = (8,8))

if mode == "D" : 
    if renorm == False : 
        Dcov_20_1_TE_y = np.linalg.inv(np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseY.npy"))
        Dcorr_TEy = corr_matrix(Dcov_20_1_TE_y)
    elif renorm == True : 
        Dcov_20_1_TE_y = np.linalg.inv(np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseY_R.npy"))
        Dcorr_TEy = corr_matrix(Dcov_20_1_TE_y)
    plt.pcolor(ks_power, ks_power, Dcorr_TEy, alpha = 0.6)
    plt.title(r"Decaying mode", fontsize = 24)
elif mode == "G" :
    Gcov_20_1_TE_y = np.linalg.inv(np.load("../Data/G_Data/fish_numks20_fsky1.00_TE_noiseY.npy"))
    Gcorr_TEy = corr_matrix(Gcov_20_1_TE_y)
    plt.pcolor(ks_power, ks_power, Gcorr_TEy, alpha = 0.6)
    plt.title(r"Growing mode", fontsize = 24)

cb = plt.colorbar()
cb.ax.tick_params(labelsize=24)
plt.xticks(ks_power)
plt.yticks(ks_power)
plt.xlabel(r'k Mpc$^{-1}$', fontsize = 24)
plt.ylabel(r'k Mpc$^{-1}$', fontsize = 24)
plt.xscale('log')
plt.yscale('log')
plt.tick_params('both', labelsize = 24)
plt.tight_layout()
if mode == "G" : 
    plt.savefig("G_plots/corr_G.pdf")
if mode == "D" : 
    if renorm == False : 
        plt.savefig("D_plots/corr_D.pdf")
    if renorm == True : 
        plt.savefig("D_plots/corr_D_R.pdf")
plt.show()
