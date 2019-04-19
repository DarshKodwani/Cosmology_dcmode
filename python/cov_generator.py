import matplotlib.pyplot as plt
import numpy as np
from classy import Class

'''
Covariance uses fiducial cosmology thus we use the fiducial parameters. 
This file does not require ANY MODIFICATION to class and should have no input for the decaying mode.
'''

#Fiducial cls from class

params = { 'output': 'tCl pCl tpCl','lensing': 'no','A_s' : 2.3e-9,'h' : 0.6711,'dAmp_k' : 0,'omega_b' : 0.022068,'omega_cdm' : 0.12029}
lmax = 2500

cosmo = Class()
cosmo.set(params)
cosmo.compute()
fullcl = cosmo.raw_cl(lmax)
l = fullcl['ell'][2:]
factor = l*(l+1)/(2*np.pi)

TT = fullcl['tt'][2:]
EE = fullcl['ee'][2:]
TE = fullcl['te'][2:]

plt.loglog(l,factor*TT, label = 'TT')
plt.loglog(l,factor*EE, label = 'EE')
plt.loglog(l,factor*TE, label = 'TE')
plt.legend()
plt.savefig("Cls_usedincov.pdf")


#Noise spectra: From table VII in 1206.2832

sigma_t =6.82
sigma_p = 10.9120
beam_amin = 9.5

sigma2_t_radians = (sigma_t/(2.725*1E6*180*60/np.pi))**2
sigma2_p_radians = (sigma_p/(2.725*1E6*180*60/np.pi))**2
beam_radians = beam_amin*np.pi/(180*60)/(2*np.sqrt(2*np.log(2)))

nltt = sigma2_t_radians*np.exp(l*(l+1)*beam_radians**2)

plt.loglog(l, TT, label='TT')
plt.loglog(l ,nltt, label = 'noiseTT')
plt.legend()
plt.savefig("noise_TT.pdf")
