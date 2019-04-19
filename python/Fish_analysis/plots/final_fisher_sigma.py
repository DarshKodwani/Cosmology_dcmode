import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors, ticker, cm
import numpy as np
import sys

renorm = True
#Import ks

ks_arr = np.load("../Data/G_Data/karr_numks20.npy")
ks_full = ks_arr[0]
ks_bins = ks_arr[1]
ks_power = ks_full[ks_bins]

#Import fishers

if renorm == False :
    Dfish_20_1_T_n = np.load("../Data/D_Data/fish_numks20_fsky1.00_T_noiseN.npy")
    Dfish_20_1_T_y = np.load("../Data/D_Data/fish_numks20_fsky1.00_T_noiseY.npy")
    Dfish_20_1_TE_n = np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseN.npy")
    Dfish_20_1_TE_y = np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseY.npy")
if renorm == True :
    Dfish_20_1_T_n = np.load("../Data/D_Data/fish_numks20_fsky1.00_T_noiseN_R.npy")
    Dfish_20_1_T_y = np.load("../Data/D_Data/fish_numks20_fsky1.00_T_noiseY_R.npy")
    Dfish_20_1_TE_n = np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseN_R.npy")
    Dfish_20_1_TE_y = np.load("../Data/D_Data/fish_numks20_fsky1.00_TE_noiseY_R.npy")

Gfish_20_1_T_n = np.load("../Data/G_Data/fish_numks20_fsky1.00_T_noiseN.npy")
Gfish_20_1_T_y = np.load("../Data/G_Data/fish_numks20_fsky1.00_T_noiseY.npy")
Gfish_20_1_TE_n = np.load("../Data/G_Data/fish_numks20_fsky1.00_TE_noiseN.npy")
Gfish_20_1_TE_y = np.load("../Data/G_Data/fish_numks20_fsky1.00_TE_noiseY.npy")

#Plots
fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (20,7))
"""
ax[0,0].plot(ks_power, np.diag(Dfish_20_1_T_n), label = "Temp, Cosmic variance", color = "blue", marker = "o", alpha = 0.4)
ax[0,0].plot(ks_power, np.diag(Dfish_20_1_T_y), label = "Temp, Planck", color = "blue", ls = '--', marker = "x", alpha = 0.4)
ax[0,0].plot(ks_power, np.diag(Dfish_20_1_TE_n), label = "Temp+Pol, Cosmic variance", color = "red", marker = "o", alpha = 0.4)
ax[0,0].plot(ks_power, np.diag(Dfish_20_1_TE_y), label = "Temp+Pol, Planck", color = "red", ls = '--', marker = "x", alpha = 0.4)
ax[0,0].set_xscale('log')
ax[0,0].set_yscale('log')
ax[0,0].set_xlim([ks_power[0], ks_power[-1]])
ax[0,0].set_title('Fisher information for Decaying modes')
ax[0,0].set_xlabel(r'k [Mpc$^{-1}$]')
ax[0,0].set_ylabel(r'$F_{diag}$')
ax[0,0].legend()

ax[0,1].plot(ks_power, np.diag(Gfish_20_1_T_n), label = "Temp, Cosmic variance", color = "blue", marker = "o", alpha = 0.4)
ax[0,1].plot(ks_power, np.diag(Gfish_20_1_T_y), label = "Temp, Planck", color = "blue", ls = '--', marker = "x", alpha = 0.4)
ax[0,1].plot(ks_power, np.diag(Gfish_20_1_TE_n), label = "Temp+Pol, Cosmic variance", color = "red", marker = "o", alpha = 0.4)
ax[0,1].plot(ks_power, np.diag(Gfish_20_1_TE_y), label = "Temp+Pol, Planck", color = "red", ls = '--', marker = "x", alpha = 0.4)
ax[0,1].set_xscale('log')
ax[0,1].set_yscale('log')
ax[0,1].set_xlim([ks_power[0], ks_power[-1]])
ax[0,1].set_title('Fisher information for Growing modes')
ax[0,1].set_xlabel(r'k [Mpc$^{-1}$]')
ax[0,1].set_ylabel(r'$F_{diag}$')
#ax[0,1].legend()
"""
ax[0].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_n))), label = "Temp, Cosmic variance", color = "blue", marker = "o", alpha = 0.4)
ax[0].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_y))), label = "Temp, Planck", color = "blue", ls = '--', marker = "x", alpha = 0.4)
ax[0].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_n))), label = "Temp+Pol, Cosmic variance", color = "red", marker = "o", alpha = 0.4)
ax[0].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_y))), label = "Temp+Pol, Planck", color = "red", ls = '--', marker = "x", alpha = 0.4)
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlim([ks_power[0], ks_power[-1]])
ax[0].set_title('Errors for Decaying modes', fontsize = 24)
ax[0].set_xlabel(r'k [Mpc$^{-1}$]', fontsize = 16)
ax[0].set_ylabel(r'$\sigma$', fontsize = 16)
ax[0].tick_params('both', labelsize = 15)

ax[1].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_n))), label = "Temp, Cosmic variance", color = "blue", marker = "o", alpha = 0.4)
ax[1].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_y))), label = "Temp, Planck", color = "blue", ls = '--', marker = "x", alpha = 0.4)
ax[1].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_n))), label = "Temp+Pol, Cosmic variance", color = "red", marker = "o", alpha = 0.4)
ax[1].plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_y))), label = "Temp+Pol, Planck", color = "red", ls = '--', marker = "x", alpha = 0.4)
ax[1].set_xscale('log')
ax[1].set_yscale('log')
ax[1].set_xlim([ks_power[0], ks_power[-1]])
ax[1].set_title('Errors for Growing modes', fontsize = 24)
ax[1].set_xlabel(r'k [Mpc$^{-1}$]', fontsize = 16)
ax[1].set_ylabel(r'$\sigma$', fontsize = 16)
ax[1].legend(fontsize = 15)
ax[1].tick_params('both', labelsize = 15)

#plt.subplots_adjust(hspace = 0.4)
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
#plt.tight_layout()
if renorm == True :
    plt.savefig("fisher_sigma_R.pdf")
if renorm == False :
    plt.savefig("fisher_sigma.pdf")
plt.show()
