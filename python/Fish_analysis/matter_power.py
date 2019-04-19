import matplotlib.pyplot as plt
import numpy as np
from classy import Class
import sys
from scipy.interpolate import interp1d

lmax = 2500
A_grow = 2.3e-9
epsilon_decay = 0.1*A_grow
dAMP_grow = A_grow/100.
dAMP_decay = epsilon_decay/100.

params_grow_fid = { 
    'output': 'mPk',
#    'non linear' : 'halofit',
    'lensing': 'no',
    'A_s' : A_grow,
    'h' : 0.6711,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

params_decay_fid = { 
    'output': 'mPk',
#    'non linear' : 'halofit', 
    'lensing': 'no',
    'n_addcs': 1.,
    'f_addcs' : .2,
    'alpha_addcs': 0.01,
    'phi_addcs': 0.,
    'h' : 0.6711,
    'ic' : 'addcs',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

#Fid Cls

cosmo_grow = Class()
cosmo_grow.set(params_grow_fid)
cosmo_grow.compute()
cosmo_d = Class()
cosmo_d.set(params_decay_fid)
cosmo_d.compute()
cosmo_d.empty()
pk_grow = []
pk_decay_f1 = []
pk_decay_f08 = []
pk_decay_f06 = []
pk_decay_f04 = []
pk_decay_f02 = []
z_used = 0.
ks = np.linspace(1e-3, 1e-1, 1e3)

"""
for i in [0.8, 0.6, 0.4, 0.2] : 
    cosmo_d.set({'f_addcs' : i})
    cosmo_d.compute()
    cosmo_d.empty()
"""

for j in ks : 
    pk_grow.append(cosmo_grow.pk(j, 0))    
    pk_decay_f1.append(cosmo_d.pk(j, 0))
    

#print(pk_decay)
pk_ginterp = interp1d(ks, pk_grow)
pk_dinterp = interp1d(ks, pk_decay_f1)

cosmo_grow.empty()

plt.loglog(ks, pk_ginterp(ks), label = "growing")
plt.loglog(ks, pk_dinterp(ks), label = "decaying, f = 0.2, $\phi$ = 0")
plt.xlabel("k [Mpc$^{-1}$]")
plt.ylabel("P(k)")
plt.legend()
plt.savefig("matter_decay.pdf")
plt.show()
    
