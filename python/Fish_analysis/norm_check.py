import matplotlib.pyplot as plt
import numpy as np
from classy import Class
import sys
from scipy.interpolate import interp1d

numks = 20

Trenorm_data = np.load("Data/renorm_temp.npy")
Prenorm_data = np.load("Data/renorm_pol.npy")
lsrenorm_data = np.load("Data/renorm_ls.npy")
Trenorm = interp1d(lsrenorm_data, Trenorm_data)
Prenorm = interp1d(lsrenorm_data, Prenorm_data)

#plt.plot(lsrenorm_data, Trenorm(lsrenorm_data))
#plt.show()

lmax = 2500
A_grow = 2.3e-9
A_decay = A_grow
epsilon_decay = 0.1*A_grow
dAMP_grow = A_grow/100.
dAMP_decay = epsilon_decay/100.

params_grow_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'A_s' : A_grow,
    'h' : 0.6711,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

params_decay_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
#    'A_s' : A_grow,  #NEED TO CHECK THESE ARE THE PARAMS WE USE!
#    'f_addcs' : 0.2
    'n_addcs': 1.,
    'alpha_addcs': 0.,
    'phi_addcs': 0.,
    'h' : 0.6711,
    'ic' : 'addcs',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

#Decay fid Cls

cosmo_D = Class()
cosmo_D.set(params_decay_fid)
cosmo_D.compute()
cl_D = cosmo_D.raw_cl(lmax)
TT_D = cl_D['tt'][2:]
EE_D = cl_D['ee'][2:]
TE_D = cl_D['te'][2:] 
ls = cl_D['ell'][2:] 
cl_fid_array = np.array([ls, TT_D, EE_D, TE_D])
Trenorm = Trenorm(ls)
Prenorm = Prenorm(ls)
cosmo_D.empty()

#Decay fid Cls

cosmo_G = Class()
cosmo_G.set(params_grow_fid)
cosmo_G.compute()
cl_G = cosmo_G.raw_cl(lmax)
TT_G = cl_G['tt'][2:]
EE_G = cl_G['ee'][2:]
TE_G = cl_G['te'][2:] 
ls = cl_G['ell'][2:] 
cl_fid_array = np.array([ls, TT_G, EE_G, TE_G])
cosmo_G.empty()

plt.plot(ls, ls*(ls+1)*TT_D/(2*np.pi), label = "TT_D")
plt.plot(ls, ls*(ls+1)*TT_D*Trenorm/(2*np.pi), label = "TT_D_renorm")
plt.plot(ls, ls*(ls+1)*TT_G/(2*np.pi), label = "TT_G")
plt.plot(ls, Trenorm, label = 'Renorm factor')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()
