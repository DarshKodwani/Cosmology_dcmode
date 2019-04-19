import matplotlib.pyplot as plt
import numpy as np
from classy import Class

k = 1 # 1/Mpc

cosmo = {'output' : 'mPk', 'k_output_values' : k, 'h' : 0.67556, 'omega_b' : 0.022032, 'omega_cdm' : 0.12038, 'A_s' : 2.215e-9, 'n_s' : 0.9619, 'tau_reio' : 0.0925, 'YHe' : 0.246, 'compute damping scale' : 'yes', 'gauge' : 'newtonian', 'ic' : 'ad&addcs', 'f_addcs' : 0.0001, 'n_addcs' : 1., 'alpha_addcs' : 0., 'phi_addcs' : 0.785}

M = Class()
M.set(cosmo)
M.compute()
M.struct_cleanup
M.empty()

all_k = M.get_perturbations()
one_k = all_k['scalar'][0]
phi = one_k['phi']
tau = one_k['tau [Mpc]']
a = one_k['a']

#plt.xlim(10**(-1), 10**1)
plt.loglog(tau, phi)
plt.show()
