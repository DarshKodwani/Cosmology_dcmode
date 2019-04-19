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
eps = 10 #Decaying mode overall bin amplitude

fig = plt.figure(figsize = (15,10))
ax0 = fig.add_axes([0.1, 0.5, 0.8, 0.4])
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.4])

ax0.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_n))), label = "Decaying mode Temp, Cosmic variance", color = "blue", marker = "o", alpha = 0.4)
ax0.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_y))), label = "Decaying mode Temp, Planck", color = "blue", ls = '--', marker = "x", alpha = 0.4)
ax0.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_n))), label = "Decaying mode Temp+Pol, Cosmic variance", color = "blue", ls = '-.', marker = "o", alpha = 0.4)
ax0.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_y))), label = "Decaying mode Temp+Pol, Planck", color = "blue", ls = ':', marker = "x", alpha = 0.4)

ax0.plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_n))), label = "Growing mode Temp, Cosmic variance", color = "red", marker = "o", alpha = 0.4)
ax0.plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_y))), label = "Growing mode Temp, Planck", color = "red", ls = '--', marker = "x", alpha = 0.4)
ax0.plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_n))), label = "Growing mode Temp+Pol, Cosmic variance", ls = '-.', color = "red", marker = "o", alpha = 0.4)
ax0.plot(ks_power, np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_y))), label = "Growing mode Temp+Pol, Planck", color = "red", ls = ':', marker = "x", alpha = 0.4)

ax0.set_xscale('log')
ax0.set_yscale('log')
ax0.set_xlim([ks_power[0], ks_power[-1]])
#ax0.set_ylim([1e-14, 1e4])
ax0.set_title('Errors for adiabatic modes', fontsize = 24)
ax0.set_xlabel(r'k [Mpc$^{-1}$]', fontsize = 20)
ax0.set_ylabel(r'$\sigma[K]$', fontsize = 20)
ax0.set_xticklabels([])
ax0.tick_params('both', labelsize = 15)

lines = ax0.get_lines()
legend1 = ax0.legend([lines[i] for i in [0,1,2,3]], ["Temp Cosmic variance", "Temp Planck", "Temp+Pol Cosmic variance", "Temp+Pol Planck"], fontsize = 16)
#legend2 = ax0.legend([lines[i] for i in [0,4]], ["Decaying mode", "Growing mode"], fontsize = 12, bbox_to_anchor=(0.7,0.25))
legend2 = ax0.legend([lines[i] for i in [0,4]], ["Decaying mode", "Growing mode"], fontsize = 16, loc = 'upper center', bbox_to_anchor = (0.5, 0.6))
ax0.add_artist(legend1)
ax0.add_artist(legend2)

ax1.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_n)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_n))), label = "Temp Cosmic variance", color = 'black')
ax1.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_n)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_n))), label = "Temp+Pol Cosmic variance", color = 'black', ls = '--')
ax1.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_y)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_y))), label = "Temp Planck", color = 'black', ls = '-.')
ax1.plot(ks_power, eps*np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_y)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_y))), label = "Temp+Pol Planck", color = 'black', ls = ':')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlim([ks_power[0], ks_power[-1]])
#ax1.set_ylim([1e-11, 1e3])
ax1.set_xlabel(r'k [Mpc$^{-1}$]', fontsize = 16)
ax1.set_ylabel(r'$\frac{\sigma_{Decay}}{\sigma_{Grow}}$', fontsize = 20)
ax1.tick_params('both', which = 'major',  labelsize = 16)
ax1.legend(fontsize = 16)

ax1.axvline(3e-4, c = 'grey')
ax0.axvline(3e-4, c = 'grey')
ax1.axhline(1, c = 'g')
ax1.text(3.2*1e-4, 2.1e-4, 'Horizon size today', fontsize = 16, rotation = 90)

#ax1.axvline(3e-3, c = 'grey')
#ax0.axvline(3e-3, c = 'grey')
#ax1.text(3.2*1e-3, 1e-4, 'Horizon size cmb', fontsize = 16, rotation = 90)

"""
plt.loglog(ks_power, 1- np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_n)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_n))), label = "Temp Cosmic variance", color = 'black')
plt.loglog(ks_power, 1- np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_T_y)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_T_y))), label = "Temp Planck", color = 'black', ls = '--')
plt.loglog(ks_power, 1- np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_n)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_n))), label = "Temp+pol Cosmic variance", color = 'black', ls = '-.')
plt.loglog(ks_power, 1- np.sqrt(np.diag(np.linalg.inv(Dfish_20_1_TE_y)))/np.sqrt(np.diag(np.linalg.inv(Gfish_20_1_TE_y))), label = "Temp+pol Planck", color = 'black', ls = ':')
plt.legend()
plt.savefig("oneminus.pdf")
"""

#plt.tight_layout()
plt.savefig("combined_adiabatic_errors.pdf")
plt.show()
